import os
import re
import json
import time
import numpy
import scipy
import pprint
import shutil
import pathlib
import datetime

from pyicat_plus.client.main import IcatClient

from edna2.tasks.AbstractTask import AbstractTask
from edna2.tasks.WaitFileTask import WaitFileTask
from edna2.tasks.ControlDozor import ControlDozor
from edna2.tasks.PhenixTasks import DistlSignalStrengthTask
from edna2.tasks.DIALSFindSpots import DIALSFindSpots
from edna2.tasks.H5ToCBFTask import H5ToCBFTask
from edna2.tasks.ReadImageHeader import ReadImageHeader
from edna2.tasks.DozorM2 import DozorM2

from edna2 import config
from edna2.utils import UtilsPath
from edna2.utils import UtilsICAT
from edna2.utils import UtilsImage
from edna2.utils import UtilsIspyb
from edna2.utils import UtilsLogging

from edna2.tasks.ISPyBTasks import ISPyBRetrieveDataCollection

logger = UtilsLogging.getLogger()

DEFAULT_MIN_IMAGE_SIZE = 1000000
DEFAULT_WAIT_FILE_TIMEOUT = 300


class ImageQualityIndicators(AbstractTask):
    """
    This task controls the plugins that generate image quality indicators.
    """

    def __init__(self, inData, workingDirectorySuffix=None):
        AbstractTask.__init__(self, inData, workingDirectorySuffix)
        self.beamline = None
        self.directory = None
        self.template = None
        self.doSubmit = None
        self.runDozorM2 = None
        self.doDistlSignalStrength = None
        self.doDialsFindSpots = None
        self.isFastMesh = None
        self.listImage = None
        self.batchSize = None
        self.minImageSize = None
        self.waitFileTimeout = None
        self.doIspybUpload = None
        self.dataCollectionId = None
        self.doIcatUpload = None
        self.overlap = None
        self.doPlot = None
        self.do_assess_centering = None

    def run(self, inData):
        dict_centring = None
        list_image_quality_indicators = []
        list_control_dozor_all_file = []
        start_time = datetime.datetime.now().astimezone().isoformat()
        # Initialize parameters
        self.init(inData)
        # Set up batch list
        list_of_batches = self.createBatchList(inData)
        out_data = dict()
        list_dozor_task, distl_results, dials_tasks = self.runDozorDistlDials(
            list_of_batches
        )
        if not self.isFailure():
            (
                list_image_quality_indicators,
                list_control_dozor_all_file,
            ) = self.synchronizeDozor(list_dozor_task, distl_results, dials_tasks)
            # Assemble all controlDozorAllFiles into one
            imageQualityIndicatorsDozorAllFile = self.createDozorAllFile(
                list_control_dozor_all_file
            )
            out_data["dozorAllFile"] = imageQualityIndicatorsDozorAllFile
        if self.runDozorM2:
            self.executeDozorM2(list_control_dozor_all_file)
        out_data["imageQualityIndicators"] = list_image_quality_indicators
        # Check if assess centring
        if self.do_assess_centering:
            dict_centring = self.assess_centring(list_image_quality_indicators)
            out_data["centring"] = dict_centring
        end_time = datetime.datetime.now().astimezone().isoformat()
        # Make plot if we have a data collection id
        if self.doPlot:
            working_directory = self.getWorkingDirectory()
            dozor_plot_path, dozor_csv_path = self.makePlot(
                inData["dataCollectionId"], out_data, working_directory
            )
            logger.info("Checking if doIspybUpload")
            if self.doIspybUpload:
                logger.debug("doIspybUpload")
                self.storeDataOnPyarch(
                    inData["dataCollectionId"],
                    dozor_plot_path=dozor_plot_path,
                    dozor_csv_path=dozor_csv_path,
                    workingDirectory=working_directory,
                )

            if self.doIcatUpload:
                logger.debug("doIcatUpload")
                self.uploadDataToIcat(
                    working_directory=working_directory,
                    raw=str(self.directory),
                    dozor_csv_path=dozor_csv_path,
                    dozor_plot_path=dozor_plot_path,
                    start_time=start_time,
                    end_time=end_time,
                    dict_centring=dict_centring,
                )

        return out_data

    def init(self, inData):
        self.beamline = inData.get("beamline", None)
        self.doSubmit = inData.get("doSubmit", False)
        self.runDozorM2 = False
        self.doTotalIntensity = inData.get("doTotalIntensity", False)
        self.doDistlSignalStrength = inData.get("doDistlSignalStrength", False)
        self.doDialsFindSpots = inData.get("doDialsFindSpots", False)
        self.isFastMesh = inData.get("fastMesh", True)
        self.listImage = inData.get("image", [])
        self.batchSize = inData.get("batchSize", 100)
        self.doIspybUpload = inData.get("doIspybUpload", False)
        self.dataCollectionId = inData.get("dataCollectionId", None)
        self.doIcatUpload = inData.get("doIcatUpload", False)
        self.doPlot = inData.get("doPlot", False)
        self.do_assess_centering = inData.get("doAssessCentring", False)
        self.new_master_path = None
        # Configurations
        self.minImageSize = config.get(
            self, "minImageSize", default=DEFAULT_MIN_IMAGE_SIZE
        )
        self.waitFileTimeOut = config.get(
            self, "waitFileTimeOut", default=DEFAULT_WAIT_FILE_TIMEOUT
        )
        if self.dataCollectionId is not None:
            ispybInData = {"dataCollectionId": self.dataCollectionId}
            ispybTask = ISPyBRetrieveDataCollection(inData=ispybInData)
            ispybTask.execute()
            dataCollection = ispybTask.outData
            inData["directory"] = dataCollection["imageDirectory"]
            inData["template"] = dataCollection["fileTemplate"].replace("%04d", "####")
            inData["startNo"] = dataCollection["startImageNumber"]
            inData["endNo"] = (
                dataCollection["startImageNumber"]
                + dataCollection["numberOfImages"]
                - 1
            )
            self.overlap = dataCollection["overlap"]
        else:
            self.overlap = inData.get("overlap", 0.0)
        if abs(self.overlap) > 0:
            self.hasOverlap = True
        else:
            self.hasOverlap = False

    def getInDataSchema(self):
        return {
            "type": "object",
            "properties": {
                "beamline": {"type": "string"},
                "runDozorM2": {"type": "boolean"},
                "doTotalIntensity": {"type": "boolean"},
                "doDistlSignalStrength": {"type": "boolean"},
                "doDialsFindSpots": {"type": "boolean"},
                "doIndexing": {"type": "boolean"},
                "doIspybUpload": {"type": "boolean"},
                "processDirectory": {"type": "string"},
                "image": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "batchSize": {"type": "integer"},
                "fastMesh": {"type": "boolean"},
                "wedgeNumber": {"type": "integer"},
                "directory": {"type": "string"},
                "template": {"type": "string"},
                "startNo": {"type": "integer"},
                "endNo": {"type": "integer"},
                "dataCollectionId": {"anyOf": [{"type": "integer"}, {"type": "null"}]},
                "overlap": {"type": "number"},
                "doPlot": {"type": "boolean"},
                "doAssessCentering": {"type": "boolean"},
            },
        }

    def getOutDataSchema(self):
        return {
            "type": "object",
            "required": ["imageQualityIndicators"],
            "properties": {
                "imageQualityIndicators": {
                    "type": "array",
                    "items": {"$ref": self.getSchemaUrl("imageQualityIndicators.json")},
                },
                "inputDozor": {"type": "number"},
                "dozorAllFile": {"type": "string"},
            },
        }

    def createBatchList(self, inData):
        listOfBatches = []
        listOfImagesInBatch = []
        if len(self.listImage) == 0:
            self.directory = pathlib.Path(inData["directory"])
            self.template = inData["template"]
            tmp_template = self.template.replace("####", "%04d")
            startNo = inData["startNo"]
            self.firstImage = pathlib.Path(self.directory) / (tmp_template % startNo)
            endNo = inData["endNo"]
            for index in range(startNo, endNo + 1):
                listOfImagesInBatch.append(index)
                if len(listOfImagesInBatch) == self.batchSize or index == 9999:
                    listOfBatches.append(listOfImagesInBatch)
                    listOfImagesInBatch = []
        else:
            self.firstImage = pathlib.Path(self.listImage[0])
            self.directory = self.firstImage.parent
            self.template = UtilsImage.getTemplate(self.firstImage)
            for image in self.listImage:
                imageNo = UtilsImage.getImageNumber(image)
                listOfImagesInBatch.append(imageNo)
                if len(listOfImagesInBatch) == self.batchSize:
                    listOfBatches.append(listOfImagesInBatch)
                    listOfImagesInBatch = []
        if len(listOfImagesInBatch) > 0:
            listOfBatches.append(listOfImagesInBatch)
        return listOfBatches

    def runDozorDistlDials(self, listOfBatches):
        #
        # Loop over batches:
        # - Wait for all files in batch
        # - Run:
        #       Dozor,
        #       DistlSignalStrength (if required)
        #       DIALS find_spots (if required)
        #   in parallel
        dozor_tasks = []
        distl_results = {}
        dials_tasks = []
        template4d = re.sub("#+", "{0:04d}", self.template)
        template6d = re.sub("#+", "{0:06d}", self.template)
        for index, images_in_batch in enumerate(listOfBatches):
            distl_tasks = []
            listOfH5FilesInBatch = []
            image_no = images_in_batch[-1]
            # Wait for last image
            image_path = self.directory / template4d.format(image_no)
            logger.debug("Waiting for path: {0}".format(image_path))
            self.waitForImagePath(
                imagePath=image_path,
                batchSize=self.batchSize,
                isFastMesh=self.isFastMesh,
                minImageSize=self.minImageSize,
                waitFileTimeOut=self.waitFileTimeOut,
                listofH5FilesInBatch=listOfH5FilesInBatch,
            )
            logger.debug("Done waiting for path: {0}".format(image_path))
            if not self.isFailure():
                # Determine start and end image no
                batchStartNo = images_in_batch[0]
                batchEndNo = images_in_batch[-1]
                dozorTemplate = self.template
                # Convert images to CBF if necessary
                if self.doDistlSignalStrength and dozorTemplate.endswith(".h5"):
                    inDataH5ToCBF = {
                        "startImageNumber": batchStartNo,
                        "endImageNumber": batchEndNo,
                        "hdf5ImageNumber": 1,
                        "hdf5File": self.directory / template4d.format(batchStartNo),
                    }
                    h5ToCBFTask = H5ToCBFTask(inData=inDataH5ToCBF)
                    h5ToCBFTask.start()
                # Run Control Dozor
                inDataControlDozor = {
                    "template": dozorTemplate,
                    "directory": self.directory,
                    "startNo": batchStartNo,
                    "endNo": batchEndNo,
                    "batchSize": self.batchSize,
                    "doSubmit": self.doSubmit,
                    "runDozorM2": False,
                    "doIspybUpload": self.doIspybUpload,
                    "overlap": self.overlap,
                    "doTotalIntensity": self.doTotalIntensity,
                    "prepareDozorAllFile": True,
                }
                if self.beamline is not None:
                    inDataControlDozor["beamline"] = self.beamline
                controlDozor = ControlDozor(
                    inDataControlDozor,
                    workingDirectorySuffix="{0:04d}_{1:04d}".format(
                        batchStartNo, batchEndNo
                    ),
                )
                controlDozor.start()
                dozor_tasks.append(
                    (controlDozor, inDataControlDozor, list(images_in_batch))
                )
                # Check if we should run distl.signalStrength
                if self.doDistlSignalStrength:
                    if image_path.suffix == ".h5":
                        h5ToCBFTask.join()
                    for image_no in images_in_batch:
                        image_path = self.directory / template4d.format(image_no)
                        if image_path.suffix == ".h5":
                            image_path = str(
                                self.directory / template6d.format(image_no)
                            )
                            image_path = image_path.replace(".h5", ".cbf")
                        inDataDistl = {
                            "referenceImage": str(image_path),
                        }
                        distlTask = DistlSignalStrengthTask(
                            inData=inDataDistl,
                            workingDirectorySuffix=image_no,
                        )
                        # logger.info(f"Running {image_path}")
                        distlTask.start()
                        # logger.info(f"After running {image_path}")
                        distl_tasks.append((distlTask, image_path))
                # Check if we should run DIALS find_spots
                if self.doDialsFindSpots and image_path.suffix == ".h5":
                    if self.new_master_path is None:
                        first_image = UtilsImage.template_to_image_name(
                            self.template, 1
                        )
                        h5_master, _, _ = UtilsImage.getH5FilePath(
                            first_image, hasOverlap=False, isFastMesh=True
                        )
                        input_master_file = self.directory / h5_master
                        self.new_master_path = (
                            self.getWorkingDirectory() / "new_master.h5"
                        )
                        DIALSFindSpots.fix_mesh_master_file(
                            input_master_file, self.new_master_path
                        )
                    if self.hasOverlap:
                        # Since we have overlap we must launch the DIALS task image per image
                        for image_no in images_in_batch:
                            in_data_dials = {
                                "directory": self.directory,
                                "template": self.template,
                                "startNo": image_no,
                                "endNo": image_no,
                                "doSubmit": self.doSubmit,
                                "hasOverlap": True,
                                "newMasterPath": self.new_master_path,
                            }
                            dials_task = DIALSFindSpots(
                                inData=in_data_dials,
                                workingDirectorySuffix=f"{image_no:04d}",
                            )
                            dials_task.start()
                            dials_tasks.append(dials_task)
                    else:
                        start_no = images_in_batch[0]
                        end_no = images_in_batch[-1]
                        in_data_dials = {
                            "directory": self.directory,
                            "template": self.template,
                            "startNo": start_no,
                            "endNo": end_no,
                            "doSubmit": self.doSubmit,
                            "hasOverlap": self.hasOverlap,
                        }
                        dials_task = DIALSFindSpots(
                            inData=in_data_dials,
                            workingDirectorySuffix=f"{start_no:04d}_{end_no:04d}",
                        )
                        dials_task.start()
                        dials_tasks.append(dials_task)
            for distlTask, image_path in distl_tasks:
                logger.info(f"Joining distlTask {image_path}")
                distlTask.join()
                distl_results[os.path.basename(image_path)] = dict(distlTask.outData)
        return dozor_tasks, distl_results, dials_tasks

    def executeDozorM2(self, listDozorAllFile):
        image = str(self.firstImage)
        inDataReadHeader = {
            "imagePath": [image],
            "skipNumberOfImages": True,
            "hasOverlap": self.hasOverlap,
            "isFastMesh": True,
        }
        workingDirectorySuffix = ""
        controlHeader = ReadImageHeader(
            inData=inDataReadHeader, workingDirectorySuffix=workingDirectorySuffix
        )
        controlHeader.execute()
        outDataHeader = controlHeader.outData
        subWedge = outDataHeader["subWedge"][0]
        experimentalCondition = subWedge["experimentalCondition"]
        dict_beam = experimentalCondition["beam"]
        dict_detector = experimentalCondition["detector"]
        _ = experimentalCondition["goniostat"]
        # Run dozorm2
        reject_level = 40
        phiValues = None
        nominal_beamsize_x = config.get(self, "nominal_beamsize_x")
        nominal_beamsize_y = config.get(self, "nominal_beamsize_y")
        inDataDozorM2 = {
            "detectorType": dict_detector["type"],
            "detector_distance": dict_detector["distance"],
            "wavelength": dict_beam["wavelength"],
            "orgx": dict_detector["beamPositionX"] / dict_detector["pixelSizeX"],
            "orgy": dict_detector["beamPositionY"] / dict_detector["pixelSizeY"],
            "number_row": 900,
            "number_images": 900,
            "isZigZag": False,
            "step_h": None,
            "step_v": None,
            "beam_shape": "G",
            "beam_h": nominal_beamsize_x,
            "beam_v": nominal_beamsize_y,
            "number_apertures": None,
            "aperture_size": None,
            "reject_level": reject_level,
            "list_dozor_all": listDozorAllFile,
            "phi_values": phiValues,
            "number_scans": len(listDozorAllFile),
            "first_scan_number": 1,
            "workingDirectory": self.getWorkingDirectory(),
            "isHorizontalScan": True,
            "grid_x0": None,
            "grid_y0": None,
            "loop_thickness": None,
        }
        workingDirectorySuffix = "dozorm2"
        dozorM2 = DozorM2(
            inData=inDataDozorM2, workingDirectorySuffix=workingDirectorySuffix
        )
        logger.debug("Running DozorM2...")
        logger.debug(f"workingDirectory: {self.getWorkingDirectory()}")
        dozorM2.execute()
        logger.info("DozorM2 finished: success={0}".format(dozorM2.isSuccess()))

    def synchronizeDistl(self, listDistlTask):
        listDistlResult = []
        # Synchronize all image quality indicator plugins and upload to ISPyB
        for image, distlTask in listDistlTask:
            imageQualityIndicators = {}
            if distlTask is not None:
                # distlTask.join()
                if distlTask.isSuccess():
                    outDataDistl = distlTask.outData
                    if outDataDistl is not None:
                        imageQualityIndicators = outDataDistl["imageQualityIndicators"]
            imageQualityIndicators["image"] = str(image)
            listDistlResult.append(imageQualityIndicators)
        return listDistlResult

    def synchronizeDozor(self, listDozorTask, distl_results, dials_tasks):
        listImageQualityIndicators = []
        listControlDozorAllFile = []
        for (
            controlDozor,
            inDataControlDozor,
            listBatch,
        ) in listDozorTask:
            controlDozor.join()
            # Check that we got at least one result
            if len(controlDozor.outData["imageQualityIndicators"]) == 0:
                # Run the dozor plugin again, this time synchronously
                firstImage = listBatch[0]
                lastImage = listBatch[-1]
                logger.warning(
                    "No dozor results! Re-executing Dozor for"
                    + " images {0} to {1}".format(firstImage, lastImage)
                )
                controlDozor = ControlDozor(
                    inDataControlDozor,
                    workingDirectorySuffix="{0:04d}_{1:04d}_redo".format(
                        firstImage, lastImage
                    ),
                )
                controlDozor.execute()
            listOutDataControlDozor = list(
                controlDozor.outData["imageQualityIndicators"]
            )
            if self.doDistlSignalStrength:
                for outDataControlDozor in listOutDataControlDozor:
                    image = os.path.basename(outDataControlDozor["image"])
                    image = image.replace(".h5", ".cbf")
                    if image in distl_results:
                        imageQualityIndicators = dict(outDataControlDozor)
                        imageQualityIndicators.update(
                            distl_results[image]["imageQualityIndicators"]
                        )
                        listImageQualityIndicators.append(imageQualityIndicators)
                    else:
                        listImageQualityIndicators += listOutDataControlDozor
            else:
                listImageQualityIndicators += listOutDataControlDozor
            # Create temporary lookup dictionary
            tmp_lookup_dict = {}
            for image_qulatity_indicators in listImageQualityIndicators:
                image_number_dozor = image_qulatity_indicators["number"]
                tmp_lookup_dict[image_number_dozor] = image_qulatity_indicators
            for dials_task in dials_tasks:
                dials_task.join()
                list_positions = dials_task.outData["listPositions"]
                for position in list_positions:
                    image_no = position["imageNumber"]
                    if image_no in tmp_lookup_dict:
                        image_qulatity_indicators = tmp_lookup_dict[image_no]
                        image_qulatity_indicators["dialsTotalIntensity"] = position[
                            "totalIntensity"
                        ]
                        image_qulatity_indicators["dialsNoSpots"] = position["noSpots"]
            # Check if dozorm
            if "dozorAllFile" in controlDozor.outData:
                listControlDozorAllFile.append(controlDozor.outData["dozorAllFile"])
        return listImageQualityIndicators, listControlDozorAllFile

    def createDozorAllFile(self, listControlDozorAllFile):
        imageQualityIndicatorsDozorAllFile = str(
            self.getWorkingDirectory() / "dozor_all"
        )
        os.system("touch {0}".format(imageQualityIndicatorsDozorAllFile))
        for controlDozorAllFile in listControlDozorAllFile:
            command = (
                "cat "
                + controlDozorAllFile
                + " >> "
                + imageQualityIndicatorsDozorAllFile
            )
            os.system(command)
        return imageQualityIndicatorsDozorAllFile

    @classmethod
    def getH5FilePath(cls, filePath, batchSize=1, isFastMesh=False):
        imageNumber = UtilsImage.getImageNumber(filePath)
        prefix = UtilsImage.getPrefix(filePath)
        if isFastMesh:
            h5ImageNumber = int((imageNumber - 1) / 100) + 1
            h5FileNumber = 1
        else:
            h5ImageNumber = 1
            h5FileNumber = int((imageNumber - 1) / batchSize) * batchSize + 1
        h5MasterFileName = "{prefix}_{h5FileNumber}_master.h5".format(
            prefix=prefix, h5FileNumber=h5FileNumber
        )
        h5MasterFilePath = filePath.parent / h5MasterFileName
        h5DataFileName = "{prefix}_{h5FileNumber}_data_{h5ImageNumber:06d}.h5".format(
            prefix=prefix, h5FileNumber=h5FileNumber, h5ImageNumber=h5ImageNumber
        )
        h5DataFilePath = filePath.parent / h5DataFileName
        return h5MasterFilePath, h5DataFilePath, h5FileNumber

    def waitForImagePath(
        self,
        imagePath,
        batchSize,
        isFastMesh,
        minImageSize,
        waitFileTimeOut,
        listofH5FilesInBatch,
    ):
        # Force an 'ls' in parent directory - this sometimes helps to 'unblock'
        # the file system
        os.system("ls {0} > /dev/null".format(os.path.dirname(imagePath)))
        # If Eiger, just wait for the h5 file
        if imagePath.suffix == ".h5":
            h5MasterFilePath, h5DataFilePath, hdf5ImageNumber = self.getH5FilePath(
                imagePath, batchSize=batchSize, isFastMesh=isFastMesh
            )
            if h5DataFilePath not in listofH5FilesInBatch:
                listofH5FilesInBatch.append(h5DataFilePath)
                logger.info("Eiger data, waiting for master" + " and data files...")
                inDataWaitFileTask = {
                    "file": str(h5DataFilePath),
                    "size": minImageSize,
                    "timeOut": waitFileTimeOut,
                }
                workingDirectorySuffix = h5DataFilePath.name.split(".h5")[0]
                waitFileTask = WaitFileTask(
                    inData=inDataWaitFileTask,
                    workingDirectorySuffix=workingDirectorySuffix,
                )
                logger.info("Waiting for file {0}".format(h5DataFilePath))
                logger.debug("Wait file timeOut set to %f" % waitFileTimeOut)
                waitFileTask.execute()
                time.sleep(0.1)
            if not os.path.exists(h5DataFilePath):
                errorMessage = "Time-out while waiting for image %s" % h5DataFilePath
                logger.error(errorMessage)
                self.setFailure()
        else:
            if not imagePath.exists():
                logger.info("Waiting for file {0}".format(imagePath))
                inDataWaitFileTask = {
                    "file": str(imagePath),
                    "size": minImageSize,
                    "timeOut": waitFileTimeOut,
                }
                workingDirectorySuffix = imagePath.name.split(imagePath.suffix)[0]
                waitFileTask = WaitFileTask(
                    inData=inDataWaitFileTask,
                    workingDirectorySuffix=workingDirectorySuffix,
                )
                logger.debug("Wait file timeOut set to %.0f s" % waitFileTimeOut)
                waitFileTask.execute()
            if not imagePath.exists():
                errorMessage = "Time-out while waiting for image " + str(imagePath)
                logger.error(errorMessage)
                self.setFailure()

    def createGnuPlotFile(self, workingDirectory, csvFileName, outDataImageDozor):
        with open(str(workingDirectory / csvFileName), "w") as gnuplotFile:
            gnuplotFile.write("# Data directory: {0}\n".format(self.directory))
            gnuplotFile.write(
                "# File template: {0}\n".format(self.template.replace("%04d", "####"))
            )
            gnuplotFile.write(
                "# {0:>9s}{1:>16s}{2:>16s}{3:>16s}{4:>16s}{5:>16s}\n".format(
                    "'Image no'",
                    "'Angle'",
                    "'No of spots'",
                    "'Main score (*10)'",
                    "'Spot score'",
                    "'Visible res.'",
                )
            )
            for imageQualityIndicators in outDataImageDozor["imageQualityIndicators"]:
                gnuplotFile.write(
                    "{0:10d},{1:15.3f},{2:15d},{3:15.3f},{4:15.3f},{5:15.3f}\n".format(
                        imageQualityIndicators["number"],
                        imageQualityIndicators["angle"],
                        imageQualityIndicators["dozorSpotsNumOf"],
                        10 * imageQualityIndicators["dozorScore"],
                        imageQualityIndicators["dozorSpotScore"],
                        imageQualityIndicators["dozorVisibleResolution"],
                    )
                )

    def determineMinMaxParameters(self, outDataImageDozor):
        minImageNumber = None
        maxImageNumber = None
        minAngle = None
        maxAngle = None
        minDozorValue = None
        maxDozorValue = None
        minResolution = None
        maxResolution = None
        for imageQualityIndicators in outDataImageDozor["imageQualityIndicators"]:
            if (
                minImageNumber is None
                or minImageNumber > imageQualityIndicators["number"]
            ):
                minImageNumber = imageQualityIndicators["number"]
                minAngle = imageQualityIndicators["angle"]
            if (
                maxImageNumber is None
                or maxImageNumber < imageQualityIndicators["number"]
            ):
                maxImageNumber = imageQualityIndicators["number"]
                maxAngle = imageQualityIndicators["angle"]
            if (
                minDozorValue is None
                or minDozorValue > imageQualityIndicators["dozorScore"]
            ):
                minDozorValue = imageQualityIndicators["dozorScore"]
            if (
                maxDozorValue is None
                or maxDozorValue < imageQualityIndicators["dozorScore"]
            ):
                maxDozorValue = imageQualityIndicators["dozorScore"]

            # Min resolution: the higher the value the lower the resolution
            if (
                minResolution is None
                or minResolution < imageQualityIndicators["dozorVisibleResolution"]
            ):
                # Disregard resolution worse than 10.0
                if imageQualityIndicators["dozorVisibleResolution"] < 10.0:
                    minResolution = imageQualityIndicators["dozorVisibleResolution"]
            # Max resolution: the lower the number the better the resolution
            if (
                maxResolution is None
                or maxResolution > imageQualityIndicators["dozorVisibleResolution"]
            ):
                maxResolution = imageQualityIndicators["dozorVisibleResolution"]
        plotDict = {
            "minImageNumber": minImageNumber,
            "maxImageNumber": maxImageNumber,
            "minAngle": minAngle,
            "maxAngle": maxAngle,
            "minDozorValue": minDozorValue,
            "maxDozorValue": maxDozorValue,
            "minResolution": minResolution,
            "maxResolution": maxResolution,
        }
        return plotDict

    def determinePlotParameters(self, plotDict):
        xtics = ""
        minImageNumber = plotDict["minImageNumber"]
        maxImageNumber = plotDict["maxImageNumber"]
        minAngle = plotDict["minAngle"]
        maxAngle = plotDict["maxAngle"]
        minResolution = plotDict["minResolution"]
        maxResolution = plotDict["maxResolution"]
        minDozorValue = plotDict["minDozorValue"]
        maxDozorValue = plotDict["maxDozorValue"]
        if minImageNumber is not None and minImageNumber == maxImageNumber:
            minAngle -= 1.0
            maxAngle += 1.0
        noImages = maxImageNumber - minImageNumber + 1
        if noImages <= 4:
            minImageNumber -= 0.1
            maxImageNumber += 0.1
            deltaAngle = maxAngle - minAngle
            minAngle -= deltaAngle * 0.1 / noImages
            maxAngle += deltaAngle * 0.1 / noImages
            xtics = "1"
        if maxResolution is None or maxResolution > 0.8:
            maxResolution = 0.8
        else:
            maxResolution = int(maxResolution * 10.0) / 10.0
        if minResolution is None or minResolution < 4.5:
            minResolution = 4.5
        else:
            minResolution = int(minResolution * 10.0) / 10.0 + 1
        if maxDozorValue < 0.001 and minDozorValue < 0.001:
            yscale = "set yrange [-0.5:0.5]\n    set ytics 1"
        else:
            yscale = "set autoscale  y"
        plotDict = {
            "xtics": xtics,
            "yscale": yscale,
            "minImageNumber": minImageNumber,
            "maxImageNumber": maxImageNumber,
            "minAngle": minAngle,
            "maxAngle": maxAngle,
            "minDozorValue": minDozorValue,
            "maxDozorValue": maxDozorValue,
            "minResolution": minResolution,
            "maxResolution": maxResolution,
        }
        return plotDict

    def makePlot(self, dataCollectionId, outDataImageDozor, working_directory):
        plot_file_name = "dozor_{0}.png".format(dataCollectionId)
        csv_file_name = "dozor_{0}.csv".format(dataCollectionId)
        self.createGnuPlotFile(working_directory, csv_file_name, outDataImageDozor)
        plot_dict = self.determineMinMaxParameters(outDataImageDozor)
        plot_dict = self.determinePlotParameters(plot_dict)
        gnuplot_script = """#
set terminal png
set output '{dozorPlotFileName}'
set title '{title}'
set grid x2 y2
set xlabel 'Image number'
set x2label 'Angle (degrees)'
set y2label 'Resolution (A)'
set ylabel 'Number of spots / ExecDozor score (*10)'
set xtics {xtics} nomirror
set x2tics
set ytics nomirror
set y2tics
set xrange [{minImageNumber}:{maxImageNumber}]
set x2range [{minAngle}:{maxAngle}]
{yscale}
set y2range [{minResolution}:{maxResolution}]
set key below
plot '{dozorCsvFileName}' using 1:3 title 'Number of spots' axes x1y1 with points linetype rgb 'goldenrod' pointtype 7 pointsize 1.5, \
    '{dozorCsvFileName}' using 1:4 title 'ExecDozor score' axes x1y1 with points linetype 3 pointtype 7 pointsize 1.5, \
    '{dozorCsvFileName}' using 1:6 title 'Visible resolution' axes x1y2 with points linetype 1 pointtype 7 pointsize 1.5
""".format(
            title=self.template.replace("%04d", "####"),
            dozorPlotFileName=plot_file_name,
            dozorCsvFileName=csv_file_name,
            minImageNumber=plot_dict["minImageNumber"],
            maxImageNumber=plot_dict["maxImageNumber"],
            minAngle=plot_dict["minAngle"],
            maxAngle=plot_dict["maxAngle"],
            minResolution=plot_dict["minResolution"],
            maxResolution=plot_dict["maxResolution"],
            xtics=plot_dict["xtics"],
            yscale=plot_dict["yscale"],
        )
        data_script_path = str(working_directory / "gnuplot.dat")
        with open(data_script_path, "w") as f:
            f.write(gnuplot_script)
        list_modules = config.get("Gnuplot", "modules", [])
        old_cwd = os.getcwd()
        os.chdir(str(working_directory))
        if len(list_modules) > 0:
            execute_script = "#!/bin/bash -l\n"
            for module in list_modules:
                execute_script += f"module load {module}\n"
            execute_script += f"gnuplot {data_script_path}\n"
            execute_script_path = str(working_directory / "gnuplot.sh")
            with open(execute_script_path, "w") as f:
                f.write(execute_script)
            os.chmod(execute_script_path, 0o755)
            os.system(execute_script_path)
        else:
            gnuplot = config.get(self, "gnuplot", "gnuplot")
            os.system("{0} {1}".format(gnuplot, data_script_path))
        os.chdir(old_cwd)
        dozor_plot_path = working_directory / plot_file_name
        dozor_csv_path = working_directory / csv_file_name
        return dozor_plot_path, dozor_csv_path

    @classmethod
    def storeDataOnPyarch(
        cls, dataCollectionId, dozor_plot_path, dozor_csv_path, workingDirectory
    ):
        resultsDirectory = pathlib.Path(workingDirectory) / "results"
        try:
            if not resultsDirectory.exists():
                resultsDirectory.mkdir(parents=True, mode=0o755)
            dozorPlotResultPath = resultsDirectory / dozor_plot_path.name
            dozorCsvResultPath = resultsDirectory / dozor_csv_path.name
            shutil.copy(dozor_plot_path, dozorPlotResultPath)
            shutil.copy(dozor_csv_path, dozorCsvResultPath)
        except Exception as e:
            logger.warning(
                "Couldn't copy files to results directory: {0}".format(resultsDirectory)
            )
            logger.warning(e)
        try:
            # Create paths on pyarch
            dozorPlotPyarchPath = UtilsPath.createPyarchFilePath(dozorPlotResultPath)
            dozorCsvPyarchPath = UtilsPath.createPyarchFilePath(dozorCsvResultPath)
            if not os.path.exists(os.path.dirname(dozorPlotPyarchPath)):
                os.makedirs(os.path.dirname(dozorPlotPyarchPath), 0o755)
            shutil.copy(dozorPlotResultPath, dozorPlotPyarchPath)
            shutil.copy(dozorCsvResultPath, dozorCsvPyarchPath)
            # Upload to data collection
            dataCollectionId = UtilsIspyb.setImageQualityIndicatorsPlot(
                dataCollectionId, dozorPlotPyarchPath, dozorCsvPyarchPath
            )
        except Exception as e:
            logger.warning("Couldn't copy files to pyarch.")
            logger.warning(e)

    def getBeamlineProposalFromPath(self, path):
        """ESRF specific code for extracting the beamline name and prefix from the path"""
        list_path = list(path.parts)
        if list_path[1] != "data":
            new_path = UtilsPath.stripDataDirectoryPrefix(str(path))
            list_path = pathlib.Path(new_path).parts
        beamline = None
        proposal = None
        if list_path[2] == "visitor":
            beamline = list_path[4]
            proposal = list_path[3]
        elif list_path[3] == "inhouse":
            beamline = list_path[2]
            proposal = list_path[4]
        return (beamline, proposal)

    def uploadDataToIcat(
        self,
        working_directory,
        raw,
        dozor_csv_path,
        dozor_plot_path,
        start_time,
        end_time,
        dict_centring,
    ):
        logger.debug(working_directory)
        if working_directory.parts[-2] == "nobackup":
            beamline, proposal = self.getBeamlineProposalFromPath(working_directory)
            logger.debug(beamline)
            logger.debug(proposal)
            if beamline is not None:
                dict_config = config.get_task_config("ICAT")
                metadata_urls = dict_config.get("metadata_urls", [])
                logger.debug(f"metadata_urls: {metadata_urls}")
                if len(metadata_urls) > 0:
                    client = IcatClient(metadata_urls=metadata_urls)
                    icat_directory = working_directory.parents[1]
                    gallery_directory = icat_directory / "gallery"
                    gallery_directory.mkdir(mode=0o755, exist_ok=False)
                    shutil.copy(dozor_csv_path, gallery_directory)
                    shutil.copy(dozor_plot_path, gallery_directory)
                    sample_name = None
                    metadata_path = os.path.join(raw, "metadata.json")
                    if os.path.exists(metadata_path):
                        with open(metadata_path) as f:
                            metadata = json.loads(f.read())
                        if "Sample_name" in metadata:
                            sample_name = metadata["Sample_name"]
                    if sample_name is None:
                        dir1 = os.path.dirname(raw)
                        dir1_name = os.path.basename(dir1)
                        if dir1_name.startswith("run"):
                            dir2 = os.path.dirname(dir1)
                            dir2_name = os.path.basename(dir2)
                            if dir2_name.startswith("run"):
                                sample_name = os.path.basename(os.path.dirname(dir2))
                            else:
                                sample_name = dir2_name
                        else:
                            sample_name = dir1_name
                    metadata = {
                        "Sample_name": sample_name,
                        "scanType": "qualityIndicator",
                        "Process_program": "dozor",
                        "startDate": start_time,
                        "endDate": end_time,
                    }
                    if dict_centring:
                        metadata = metadata | dict_centring
                    dataset_name = "dozor_plot"
                    logger.debug(f"icat_directory {icat_directory}")
                    logger.debug("Before store")
                    icat_beamline = UtilsICAT.getIcatBeamline(beamline)
                    logger.debug(icat_beamline)
                    logger.debug(pprint.pformat(metadata))
                    client.store_processed_data(
                        beamline=icat_beamline,
                        proposal=proposal,
                        dataset=dataset_name,
                        path=str(icat_directory),
                        metadata=metadata,
                        raw=[raw],
                    )
                    logger.debug("After store")

    def assess_centring(self, list_image_quality_indicators):
        values = [
            d["dozorScore"]
            for d in sorted(list_image_quality_indicators, key=lambda x: x["number"])
        ]
        x = numpy.arange(len(values))
        y = numpy.array(values)
        slope, intercept, r, _, _ = scipy.stats.linregress(x, y)
        residuals = y - (slope * x + intercept)
        std_dev = numpy.std(residuals)
        rsq = r**2
        is_favorable = abs(slope) < 0.5 and std_dev < 2.0
        logger.debug(f"assess_centring: stdev {std_dev} rsq {rsq} slope {slope}")
        return {
            "MXAutoprocIntegration_fit_to_line_slope": float(slope),
            "MXAutoprocIntegration_fit_to_line_r2": float(r**2),
            "MXAutoprocIntegration_fit_to_line_stdv": float(std_dev),
            "is_favorable": bool(is_favorable),
        }
