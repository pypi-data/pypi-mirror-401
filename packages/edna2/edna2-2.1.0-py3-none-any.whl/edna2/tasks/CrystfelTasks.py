import os
import sys
import json
import logging
import pathlib
import jsonschema

from pyicat_plus.client.main import IcatClient

import autocryst.saveDozor as sd
from autocryst.Image import ImageHandler as Im
from autocryst import run_crystfel

from edna2.tasks.AbstractTask import AbstractTask

from edna2.utils import UtilsICAT
from edna2.utils import UtilsPath
from edna2.utils import UtilsImage
from edna2.utils import UtilsIspyb
from edna2 import config
from edna2.utils import UtilsLogging

__authors__ = ["S. Basu", "Olof Svensson"]
__license__ = "MIT"
__date__ = "05/07/2019"

logger = UtilsLogging.getLogger()
logger.setLevel(logging.DEBUG)
logging.getLogger("pyicat_plus").setLevel(logging.DEBUG)


class ExeCrystFEL(AbstractTask):
    def getInDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "listH5FilePath": {"type": "array", "items": {"type": "string"}},
                "doCBFtoH5": {"type": "boolean"},
                "doSubmit": {"type": "boolean"},
                "detectorType": {"type": "string"},
                "batchSize": {"type": "integer"},
                "cbfFileInfo": {
                    "directory": {"type": "string"},
                    "template": {"type": "string"},
                    "startNo": {"type": "integer"},
                    "endNo": {"type": "integer"},
                    "batchSize": {"type": "integer"},
                    "listofImages": {"type": "array", "items": {"type": "string"}},
                },
                "imageQualityIndicators": {
                    "type": "array",
                    "items": {"$ref": self.getSchemaUrl("imageQualityIndicators.json")},
                },
            },
            "oneOf": [{"required": ["listH5FilePath"]}, {"required": ["cbfFileInfo"]}],
        }

    def getOutDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "first_data_path": {"type": "string"},
                "streamfile": {"type": "string"},
                "hklfile": {"type": "string"},
                "mtzfile": {"type": "string"},
                "cellpath": {"type": "string"},
                "cell_array_file": {"type": "string"},
                "centering": {"type": "string"},
                "num_indexed_frames": {"type": "integer"},
                "lattice": {"type": "string"},
                "unique_axis": {"type": "string"},
                "unit_cell": {
                    "modal_val": {"type": "array", "items": {"type": "number"}}
                },
            },
            "point_group": {"type": "string"},
            "space_group": {"type": "string"},
            "stats": {
                "resolution_limit": {"type": "number"},
                "average_num_spots": {"type": "number"},
                "spots_per_frame": {"type": "array", "items": {"type": "number"}},
                "number_hits": {"type": "integer"},
                "snr": {"type": "array", "items": {"type": "number"}},
                "ccstar": {"type": "array", "items": {"type": "number"}},
                "rsplit": {"type": "array", "items": {"type": "number"}},
                "overall_snr": {"type": "number"},
                "overall_ccstar": {"type": "number"},
                "overall_rsplit": {"type": "number"},
                "overall_multiplicity": {"type": "number"},
            },
        }

    def run(self, inData):
        # Determine data diretcory
        if "listH5FilePath" in inData:
            first_data_path = inData["listH5FilePath"][0]
        elif "cbfFileInfo" in inData:
            raise RuntimeError("Not yet implemented!")
        else:
            raise RuntimeError("No data source found inData")
        doCBFtoH5 = inData.get("doCBFtoH5", False)

        outData = {}
        if doCBFtoH5:
            dd = sd.Dozor(inData)
            dd.extract_olof_json(inData)

            headerfile = self.getWorkingDirectory() / "headers.json"
            if dd.is_success():
                os.chdir(str(self.getWorkingDirectory()))
                if not headerfile.exists():
                    with open(str(headerfile), "w") as jhead:
                        json.dump(dd.cbfheader, jhead, sort_keys=True, indent=2)
                else:
                    pass

                if dd.stacklength <= 100:
                    dd.create_stack()
                else:
                    dd.mp_stack()

                streampath, results, cell_array = self.exeIndexing(inData)
                outData = results
            else:
                self.setFailure()
                logger.error(
                    "CrystFEL Task failed due to failure of dozor packing into cxi"
                )
        else:
            os.chdir(self.getWorkingDirectory())
            streampath, results, cell_array = self.exeIndexing(inData)
            # print("unit_cell_list: ", cell_array)
            if streampath is not None and streampath.exists():
                outData = results
                outData["streamfile"] = str(streampath)
                outData["first_data_path"] = first_data_path
                logger.info(
                    f"autoCrystFEL results are dumped: {outData['crystfeloutput']}"
                )
            if len(cell_array) > 0:
                jsonName = str(self.getWorkingDirectory() / "autocryst_unitcell.json")
                with open(jsonName, "w") as f:
                    f.write(json.dumps(cell_array, default=str, indent=4))
                outData["cell_array_file"] = jsonName
            else:
                self.setFailure()
                logger.error("AutoCryst returned empty stream file")
        return outData

    @staticmethod
    def uploadDataToIcat(raw_dir, icat_dir, out_data, start_time=None, end_time=None):
        raw_path = pathlib.Path(raw_dir)
        raw = [str(raw_path)]
        icat_dir = pathlib.Path(icat_dir)
        metadata = {"scanType": "SSX", "Process_program": "CrystFEL"}
        dataset_name = "autocryst_results2"
        beamline, proposal = UtilsPath.getBeamlineProposal(raw_path)
        icat_beamline = UtilsICAT.getIcatBeamline(beamline)
        dict_config = config.get_task_config("ICAT")
        metadata_urls = dict_config.get("metadata_urls", "[]")
        logger.debug(f"metadata_urls: {metadata_urls}")
        if len(metadata_urls) > 0:
            client = IcatClient(metadata_urls=metadata_urls)
            icat_online = icat_dir / "online"
            icat_online.mkdir(mode=0o755, exist_ok=True, parents=True)

            # shutil.copy(out_data["cell_array_file"], (icat_online / "autocryst_unitcell.json"))

            metadata_path = raw_path / "metadata.json"
            if os.path.exists(metadata_path):
                with open(metadata_path) as f:
                    meta = json.loads(f.read())
            metadata["Sample_name"] = meta["Sample_name"]
            if start_time is not None:
                metadata["startDate"] = start_time
            if end_time is not None:
                metadata["endDate"] = end_time
            out_data["num_images"] = meta["num_images"]
            jsonName = "outData_for_ICAT" + ".json"
            with open(str(icat_online / jsonName), "w") as f:
                f.write(json.dumps(out_data, default=str, indent=4))

            # icat_beamline = UtilsPath.getIcatBeamline(metadata['beamline'])
            logger.info("upload begins for %s" % icat_beamline)

            client.store_processed_data(
                beamline=icat_beamline,
                proposal=proposal,
                dataset=dataset_name,
                path=str(icat_online),
                metadata=metadata,
                raw=raw,
            )
            logger.info("upload done")

        return

    def exeIndexing(self, inData):
        doCBFtoH5 = inData.get("doCBFtoH5", False)
        doSubmit = inData.get("doSubmit", True)
        in_for_crystfel = dict()

        if "listH5FilePath" in inData.keys():
            tmp = UtilsImage.getPrefix(inData["listH5FilePath"][0])
            # pp = pathlib.Path(inData["listH5FilePath"][0])
            print("prefix in crystfelTasks %s" % tmp[:-1])
            in_for_crystfel["prefix"] = inData.get("prefix", tmp[:-1])
            in_for_crystfel["detectorType"] = inData.get("detectorType", "jungfrau")
            if inData.get("detectorType", "jungfrau") == "eiger":
                in_for_crystfel["prefix"] = tmp.strip("data")
                in_for_crystfel["maxchunksize"] = 10
                FirstImage = tmp.replace("data", "master.h5")
                Image = Im(FirstImage)
                in_for_crystfel["detectorType"] = (
                    Image.imobject.headers["detector_name"][0]
                    + Image.imobject.headers["detector_name"][1]
                )
            else:
                in_for_crystfel["geometry_file"] = inData["geometry_file"]
                in_for_crystfel["threshold"] = inData.get("threshold", "1000")
                in_for_crystfel["peak_radius"] = inData.get("peak_radius", "4,5,10")
                in_for_crystfel["int_radius"] = inData.get("int_radius", "4,5,10")
                in_for_crystfel["min_snr"] = inData.get("min_snr", "5.0")
                in_for_crystfel["min_peaks"] = inData.get("min_peaks", "20")
                in_for_crystfel["max_res"] = inData.get("max_res", "1200")
                in_for_crystfel["partition"] = inData.get("partition", "mx-low")
                in_for_crystfel["unit_cell_file"] = inData.get("unit_cell_file", " ")
                in_for_crystfel["indexing_method"] = inData.get(
                    "indexing_method", "xgandalf"
                )
                in_for_crystfel["local_bg_radius"] = inData.get("local_bg_radius", "10")

            in_for_crystfel["suffix"] = UtilsImage.getSuffix(
                inData["listH5FilePath"][0]
            )
            in_for_crystfel["image_directory"] = str(
                pathlib.Path(inData["listH5FilePath"][0]).parent
            )
            in_for_crystfel["maxchunksize"] = inData.get("batchSize", 300)

        elif "cbfFileInfo" in inData.keys():
            in_for_crystfel["maxchunksize"] = inData["cbfFileInfo"].get("batchSize", 10)
            in_for_crystfel["listofImages"] = inData["cbfFileInfo"].get(
                "listofImages", []
            )
            in_for_crystfel["image_directory"] = inData["cbfFileInfo"]["directory"]
            in_for_crystfel["prefix"] = inData["cbfFileInfo"]["template"].strip(
                "####.cbf"
            )
            in_for_crystfel["suffix"] = UtilsImage.getSuffix(
                inData["cbfFileInfo"]["template"]
            )
            if len(in_for_crystfel["listofImages"]) == 0:
                in_for_crystfel["ImageRange"] = (
                    inData["cbfFileInfo"]["startNo"],
                    inData["cbfFileInfo"]["endNo"],
                )
                FirstImage = os.path.join(
                    inData["cbfFileInfo"]["directory"],
                    inData["cbfFileInfo"]["template"].replace("####", "0001"),
                )
            else:
                FirstImage = in_for_crystfel["listofImages"][0]

            Image = Im(FirstImage)
            in_for_crystfel["detectorType"] = (
                Image.imobject.headers["detector_name"][0]
                + Image.imobject.headers["detector_name"][1]
            )
        else:
            logger.error("input json must have neither listH5FilePath nor cbfFileInfo")

        if doCBFtoH5:
            cxi_all = list(self.getWorkingDirectory().glob("dozor*cxi"))
            current = len(cxi_all) - 1
            in_for_crystfel["image_directory"] = self.getWorkingDirectory()
            in_for_crystfel["prefix"] = "dozor_%d." % current
            in_for_crystfel["suffix"] = "cxi"
            in_for_crystfel["peak_search"] = "cxi"
            in_for_crystfel["peak_info"] = "/data/peakinfo"
            in_for_crystfel["maxchunksize"] = 10

        in_for_crystfel["doSubmit"] = inData.get("doSubmit", True)

        crysttask = run_crystfel.AutoCrystFEL(in_for_crystfel)
        outstream = None
        results = dict()
        cell_array = []
        try:
            jsonschema.validate(
                instance=crysttask.jshandle, schema=crysttask.getInDataSchema()
            )
            crysttask.run_indexing()
            crysttask.combine_streams(doSubmit=doSubmit)

            outstream = crysttask.getOutputDirectory() / "alltogether.stream"

            results, cell_array = crysttask.report_cell(str(outstream))
            results["crystfeloutput"] = str(crysttask.getOutputDirectory())
            results["cellpath"] = str(crysttask.getOutputDirectory())
            crysttask.write_cell_file(results)
            results["cellpath"] = str(crysttask.getOutputDirectory() / "auto.cell")

            logger.info("Indexing done; now running partialator...")

            results = crysttask.scale_merge(str(outstream), results)

            hklfile = pathlib.Path(results["hklfile"])
            if hklfile.exists():
                crysttask.crystfel2xds(str(hklfile), results)
                ascii = str(crysttask.getOutputDirectory() / "XDS_ASCII.HKL")
                crysttask.createMTZ(ascii)
                mtz = pathlib.Path(crysttask.getOutputDirectory() / "alltogether.mtz")
            if mtz.exists():
                results["mtzfile"] = str(mtz)
            else:
                logger.error(f"{hklfile} didnot exist and could not create mtz")
            crysttask.writeOutputData(results)
        except Exception as err:
            self.setFailure()
            logger.error(err)

        return outstream, results, cell_array


class CrystFEL2ISPyB(AbstractTask):
    def getInDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "first_data_path": {"type": "string"},
                "dataCollectionId": {"type": "integer"},
                "streamfile": {"type": "string"},
                "centering": {"type": "string"},
                "num_indexed_frames": {"type": "integer"},
                "lattice": {"type": "string"},
                "unique_axis": {"type": "string"},
                "unit_cell": {
                    "type": "array",
                    "items": {"type": "number"},
                },
                "point_group": {"type": "string"},
                "space_group": {"type": "string"},
                "resolution_limit": {"type": "number"},
                "average_num_spots": {"type": "number"},
            },
        }

    def getOutDataSchema(self):
        return {"type": "object", "properties": {"status": {"type": "string"}}}

    def run(self, inData):
        qm = inData["QualityMetrics"]
        dataCollection_id = inData["dataCollectionId"]
        # Create ssx_cells.json
        ssx_cells = {"unit_cells": qm["unit_cell_array"]}
        working_dir = self.getWorkingDirectory()
        ssx_cells_path = working_dir / "ssx_cells.json"
        with open(ssx_cells_path, "w") as f:
            f.write(json.dumps(ssx_cells, indent=4))
        # Create ssx_stats.json
        ssx_stats = {
            "nbHits": qm["number_hits"],
            "nbIndexed": qm["num_indexed_frames"],
            "laticeType": qm["lattice"],
            "estimatedResolution": qm["resolution_limit"],
        }
        ssx_stats_path = working_dir / "ssx_stats.json"
        with open(ssx_stats_path, "w") as f:
            f.write(json.dumps(ssx_stats, indent=4))
        # Create pyarch directory
        first_data_path = pathlib.Path(inData["first_data_path"])
        pyarch_dir = UtilsPath.createPyarchFilePath(
            first_data_path.parent / first_data_path.stem
        )
        os.makedirs(pyarch_dir, mode=0o755, exist_ok=True)
        # Copy files to pyarch
        UtilsPath.systemCopyFile(ssx_cells_path, pyarch_dir)
        ssx_cells_pyarch_path = pyarch_dir / "ssx_cells.json"
        UtilsPath.systemCopyFile(ssx_stats_path, pyarch_dir)
        ssx_stats_pyarch_path = pyarch_dir / "ssx_stats.json"
        # Upload info to ISPyB
        #
        # 1. Create AutoProcProgram entry
        auto_proc_program_id = UtilsIspyb.storeOrUpdateAutoProcProgram(
            programs="CrystFEL", commandline="indexamajig", status="SUCCESS"
        )
        # 2. Create "dummy" AutoProcIntegration entry for linking with data collection
        auto_proc_integration_id = UtilsIspyb.storeOrUpdateAutoProcIntegration(
            auto_proc_program_id=auto_proc_program_id,
            dataCollection_id=dataCollection_id,
        )
        # 3. Upload ssx_cells and ssx_stats as program attachments
        auto_proc_program_attachment_id_cells = (
            UtilsIspyb.storeOrUpdateAutoProcProgramAttachment(
                auto_proc_program_id=auto_proc_program_id,
                file_type="Result",
                file_path=ssx_cells_pyarch_path,
            )
        )
        auto_proc_program_attachment_id_stats = (
            UtilsIspyb.storeOrUpdateAutoProcProgramAttachment(
                auto_proc_program_id=auto_proc_program_id,
                file_type="Result",
                file_path=ssx_stats_pyarch_path,
            )
        )
        out_data = {
            "status": "ok",
            "pyarch_dir": pyarch_dir,
            "dataCollectionId": dataCollection_id,
            "auto_proc_program_id": auto_proc_program_id,
            "auto_proc_integration_id": auto_proc_integration_id,
            "auto_proc_program_attachment_id_cells": auto_proc_program_attachment_id_cells,
            "auto_proc_program_attachment_id_stats": auto_proc_program_attachment_id_stats,
        }
        return out_data


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)-12s %(levelname)-8s%(message)s",
        datefmt="%y-%m-%d %H:%M",
        filename="autocryst.log",
        filemode="a+",
    )
    # __main__ block to test this particular code for debugging purpose but can be used as standalone offline
    fh = open(sys.argv[1], "r")
    inData = json.load(fh)
    fh.close()
    crystfel = ExeCrystFEL(inData)

    crystfel.executeRun()
    print(crystfel.outData)
