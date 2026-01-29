import re
import h5py
import numpy
import shutil
import pathlib

from edna2.tasks.AbstractTask import AbstractTask

from edna2.utils import UtilsImage
from edna2.utils import UtilsLogging

logger = UtilsLogging.getLogger()


class DIALSFindSpots(AbstractTask):
    """
    DIALS is a sensitive and parallelizable spot/hit finder
    """

    def getInDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "directory": {"type": "string"},
                "template": {"type": "string"},
                "startNo": {"type": "number"},
                "endNo": {"type": "number"},
                "doSubmit": {"type": "boolean"},
                "hasOverlap": {"type": "boolean"},
                "newMasterPath": {"type": "string"},
            },
        }

    def getOutDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "listPositions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "imageNumber": {"type": "number"},
                            "noSpots": {"type": "number"},
                            "noSpotsNoIce": {"type": "number"},
                            "totalIntensity": {"type": "number"},
                        },
                    },
                },
                "newMasterPath": {"type": "string"},
            },
        }

    def run(self, inData):

        out_data = {}
        directory = pathlib.Path(inData["directory"])

        # Check if we have CBF or H5 data
        template = inData.get("template")
        has_overlap = inData.get("hasOverlap", False)

        # Use image range if provided
        start_no = inData.get("startNo")
        end_no = inData.get("endNo")
        if start_no is None or end_no is None or has_overlap:
            image_range = ""
            start_no = 1
        else:
            image_range = f" scan.image_range={start_no},{end_no}"

        new_master_path = inData.get("newMasterPath", None)

        if new_master_path:
            dials_template = new_master_path
        elif template.endswith("h5"):
            first_image = UtilsImage.template_to_image_name(template, start_no)
            h5_master, _, _ = UtilsImage.getH5FilePath(
                first_image, hasOverlap=has_overlap, isFastMesh=True
            )
            input_master_file = directory / h5_master
            new_master_path = self.getWorkingDirectory() / "new_master.h5"
            self.fix_mesh_master_file(input_master_file, new_master_path)
            dials_template = str(new_master_path)
        elif template.endswith("cbf"):
            dials_template = template.replace("####", "*")

        # Run DIALS import
        dials_data_path = directory / dials_template
        command_line_import = f"dials.import {dials_data_path}{image_range}"
        self.runCommandLine(
            command_line_import, list_modules=["dials"], job_name="dials_import"
        )

        # Run DIALS find_spots
        command_line_find_spots = (
            "dials.find_spots imported.expt per_image_statistics=True"
        )
        do_submit = inData.get("doSubmit", False)
        self.runCommandLine(
            command_line_find_spots,
            list_modules=["dials"],
            do_submit=do_submit,
            partition="mx",
            no_cores=20,
            job_name="dials_find_spots",
        )

        # Parse output file
        dials_find_spots_log_path = (
            self.getWorkingDirectory() / "dials_find_spots.log.txt"
        )
        list_positions = self.parseDIALSLogFile(
            dials_find_spots_log_path, start_no=start_no
        )

        out_data["listPositions"] = list_positions
        if new_master_path:
            out_data["newMasterPath"] = str(new_master_path)

        return out_data

    @staticmethod
    def parseDIALSLogFile(path_to_log_file, start_no=1):
        list_positions = []
        #
        # --------------------------------------------------------------------------------
        # Saved 991 reflections to strong.refl
        # Number of centroids per image for imageset 0:
        # +---------+----------+-----------------+-------------------+
        # |   image |   #spots |   #spots_no_ice |   total_intensity |
        # |---------+----------+-----------------+-------------------|
        # |       1 |       10 |              10 |              5163 |
        # |       2 |        4 |               4 |              8552 |
        # |       3 |        6 |               6 |              3821 |
        # +---------+----------+-----------------+-------------------+
        with open(path_to_log_file) as fd:
            list_log_lines = fd.readlines()
        do_parse_line = False
        for line in list_log_lines:
            if line.startswith("|---------+"):
                do_parse_line = True
            elif do_parse_line:
                if re.search(r"\d+ \|", line):
                    listValues = line.split()
                    image_number = int(listValues[1]) + start_no - 1
                    position = {
                        "imageNumber": image_number,
                        "noSpots": int(listValues[3]),
                        "noSpotsNoIce": int(listValues[5]),
                        "totalIntensity": int(listValues[7]),
                    }
                    list_positions.append(position)

        return list_positions

    @staticmethod
    def make_links_absolute(f, input_file):
        """Convert all external links in /entry/data to absolute paths based on input_file."""
        # Code generated by chatGPT
        master_dir = pathlib.Path(input_file).resolve().parent
        data_group = "/entry/data"

        if data_group not in f:
            print("Warning: no /entry/data group found.")
            return

        grp = f[data_group]

        # iterate names (do NOT use group.items() because that dereferences links)
        for name in list(grp.keys()):
            # get the link object without dereferencing
            link = grp.get(name, getlink=True)

            # Only handle ExternalLink objects
            if isinstance(link, h5py.ExternalLink):
                rel_filename = link.filename  # filename stored in the external link
                target_obj = link.path  # path inside the external file

                # If already absolute, skip
                p = pathlib.Path(rel_filename)
                if p.is_absolute():
                    print(
                        f"Skipping (already absolute): {name} -> {rel_filename} {target_obj}"
                    )
                    continue

                # build absolute path relative to the input master file directory
                abs_path = master_dir / rel_filename
                try:
                    # resolve without requiring the target to exist (strict=False)
                    abs_path_resolved = abs_path.resolve(strict=False)
                except TypeError:
                    # older Python versions might not support strict keyword
                    abs_path_resolved = abs_path.resolve()

                print(f"Updating link: {name} -> {abs_path_resolved} {target_obj}")

                # delete old link and recreate as ExternalLink with absolute filename
                del grp[name]
                grp[name] = h5py.ExternalLink(str(abs_path_resolved), target_obj)
            else:
                # Not an external link: could be HardLink/Dataset/Group/etc. — skip
                # (we purposely don't dereference to avoid opening external files)
                # If you want to print other link types, uncomment the line below:
                # print(f"Skipping non-external link or dataset: {name} ({type(link)})")
                continue

    @staticmethod
    def fix_mesh_master_file(input_master_path, new_master_path):
        # Code generated by chatGPT and slightly modified

        # Copy the original file
        shutil.copy(input_master_path, new_master_path)

        with h5py.File(new_master_path, "r+") as f:
            logger.info(f"Patching {new_master_path} ...")

            # 1) Convert external links to absolute (based on the input master path)
            DIALSFindSpots.make_links_absolute(f, input_master_path)

            # 2) Patch omega metadata (same behaviour as your working script)
            try:
                nframes = len(f["/entry/sample/goniometer/omega"])
            except Exception:
                nframes = 1
            print(f"Detected {nframes} frames")

            # Fake omega_start and omega_step
            omega_start = 0.0
            omega_step = 0.1
            omega = omega_start + numpy.arange(nframes) * omega_step
            omega_end = omega + omega_step

            gpath = "/entry/sample/goniometer"
            tpath = "/entry/sample/transformations"

            for path in [gpath, tpath]:
                if path not in f:
                    f.create_group(path)
                for name, data in [("omega", omega), ("omega_end", omega_end)]:
                    dset_path = f"{path}/{name}"
                    if dset_path in f:
                        del f[dset_path]
                    f.create_dataset(dset_path, data=data, dtype=numpy.float32)

            depends_path = "/entry/sample/depends_on"
            if depends_path in f:
                del f[depends_path]
            f.create_dataset(
                depends_path, data=numpy.bytes_("/entry/sample/transformations/omega")
            )

            for dset_name in ["omega", "omega_end"]:
                for base in [gpath, tpath]:
                    dset = f[f"{base}/{dset_name}"]
                    dset.attrs["units"] = numpy.bytes_("degree")
                    dset.attrs["transformation_type"] = numpy.bytes_("rotation")
                    dset.attrs["vector"] = numpy.array(
                        [1.0, 0.0, 0.0], dtype=numpy.float32
                    )
                    dset.attrs["offset"] = numpy.array(
                        [0.0, 0.0, 0.0], dtype=numpy.float32
                    )
                    dset.attrs["depends_on"] = numpy.bytes_(".")

            logger.info(
                "Patched omega metadata and updated external links successfully."
            )
            logger.info(f"Saved to {new_master_path}")
