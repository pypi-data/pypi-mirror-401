import math
import shutil
import numpy as np

from edna2.tasks.AbstractTask import AbstractTask

from edna2 import config
from edna2.utils import UtilsPath
from edna2.utils import UtilsLogging
from edna2.utils import UtilsDetector
from edna2.utils import UtilsSymmetry


logger = UtilsLogging.getLogger()


R2D = 180 / math.pi


class XDSTask(AbstractTask):
    """
    Common base class for all XDS tasks
    """

    def run(self, inData):
        logger.debug(f"Working directory: {self.getWorkingDirectory()}")
        list_modules = config.get("XDS", "modules", default=[])
        commandLine = "xds_par"
        listXDS_INP = self.generateXDS_INP(inData)
        self.writeXDS_INP(listXDS_INP, self.getWorkingDirectory())
        self.setLogFileName("xds.log")
        self.runCommandLine(commandLine, list_command=[], list_modules=list_modules)
        # Work in progress!
        outData = self.parseXDSOutput(self.getWorkingDirectory())
        if outData is None:
            self.setFailure()
        return outData

    @staticmethod
    def generateXDS_INP(in_data):
        """
        This method creates a list of XDS.INP commands
        """
        master_path = in_data["master_path"]
        name_template = master_path.replace("_master.h5", "_??????.h5")
        beam_position_x = in_data["beam_position_x"]
        beam_position_y = in_data["beam_position_y"]
        distance = round(in_data["detector_distance"], 4) * 1000  # In mm
        wavelength = round(in_data["wavelength"], 4)
        oscillation_width = in_data["oscillation_width"]
        # Config values
        detector_x_axis = config.get("XDSTask", "DIRECTION_OF_DETECTOR_X-AXIS")
        detector_y_axis = config.get("XDSTask", "DIRECTION_OF_DETECTOR_Y-AXIS")
        rotatin_axis = config.get("XDSTask", "ROTATION_AXIS")
        incident_beam_direction = config.get("XDSTask", "INCIDENT_BEAM_DIRECTION")
        # XDS detector values
        detector = in_data["detector_type"]
        dict_xds_detector = XDSTask.getXDSDetector(detector)
        nx = dict_xds_detector["nx"]
        ny = dict_xds_detector["ny"]
        pixel = dict_xds_detector["pixel"]
        name = dict_xds_detector["name"]
        minimum_valid_pixel_value = dict_xds_detector["minimumValidPixelValue"]
        overload = dict_xds_detector["overload"]
        sensor_thickness = dict_xds_detector["sensorThickness"]
        list_trusted_region = dict_xds_detector["trustedRegion"]
        list_untrusted_rectangle = dict_xds_detector["untrustedRectangle"]
        # Creation of XDS.INP
        listXDS_INP = [
            "OVERLOAD=10048500",
            f"DIRECTION_OF_DETECTOR_X-AXIS={detector_x_axis}",
            f"DIRECTION_OF_DETECTOR_Y-AXIS={detector_y_axis}",
            f"ROTATION_AXIS={rotatin_axis}",
            f"INCIDENT_BEAM_DIRECTION={incident_beam_direction}",
            f"NAME_TEMPLATE_OF_DATA_FRAMES= {name_template}",
            f"NX={nx} NY={ny} QX={pixel} QY={pixel}",
            f"ORGX={beam_position_x} ORGY={beam_position_y}",
            f"DETECTOR={name}  MINIMUM_VALID_PIXEL_VALUE={minimum_valid_pixel_value}  OVERLOAD={overload}",
            f"SENSOR_THICKNESS={sensor_thickness}",
            f"TRUSTED_REGION={list_trusted_region[0]} {list_trusted_region[1]}",
            f"DETECTOR_DISTANCE={distance}",
            f"X-RAY_WAVELENGTH={wavelength}",
            f"OSCILLATION_RANGE={oscillation_width}",
            "INDEX_QUALITY= 0.25",
            "MINIMUM_NUMBER_OF_PIXELS_IN_A_SPOT= 5",
            "INCLUDE_RESOLUTION_RANGE= 50 3.5",
        ]
        for tr in list_untrusted_rectangle:
            listXDS_INP.append(f"UNTRUSTED_RECTANGLE={tr[0]} {tr[1]} {tr[2]} {tr[3]}")
        if "spaceGroupNumber" in in_data:
            spaceGroupNumber = in_data["spaceGroupNumber"]
            cell = in_data["cell"]
            unitCellConstants = "{a} {b} {c} {alpha} {beta} {gamma}".format(**cell)
            listXDS_INP += [
                "SPACE_GROUP_NUMBER={0}".format(spaceGroupNumber),
                "UNIT_CELL_CONSTANTS={0}".format(unitCellConstants),
            ]
        list_image_range = []
        listXDS_INP += ["BACKGROUND_RANGE= 1 4"]
        list_subwedge = in_data["subwedge"]
        rotation_axis_start = min(item["axis_start"] for item in list_subwedge)
        listXDS_INP += (f"STARTING_ANGLE={rotation_axis_start}",)
        for subwedge in list_subwedge:
            axis_start = subwedge["axis_start"]
            axis_end = subwedge["axis_end"]
            image_number_start = (
                int((axis_start - rotation_axis_start) / oscillation_width) + 1
            )
            image_number_end = int((axis_end - rotation_axis_start) / oscillation_width)
            list_image_range.append([image_number_start, image_number_end])
            listXDS_INP += [f"SPOT_RANGE= {image_number_start} {image_number_end}"]
        listXDS_INP += [
            f"DATA_RANGE= {list_image_range[0][0]} {list_image_range[-1][1]}"
        ]
        for index, image_range in enumerate(list_image_range[:-1]):
            exclude_start = list_image_range[index][1] + 1
            exclude_end = list_image_range[index + 1][0] - 1
            listXDS_INP += [f"EXCLUDE_DATA_RANGE= {exclude_start} {exclude_end}"]
        if config.get("XDS", "LIB"):
            modules = config.get("XDS", "modules")
            lib_filename = config.get("XDS", "LIB")
            lib_path = UtilsPath.find_ld_library_path(modules, lib_filename)
            listXDS_INP += [f"LIB= {lib_path}"]
        return listXDS_INP

    @staticmethod
    def createSPOT_XDS(listDozorSpotFile, oscRange):
        """
              implicit none
              integer nmax
              parameter(nmax=10000000)
              real*4 x(3),j
              integer n,i,k
              real*4 xa(nmax,3),ja(nmax)
              logical new
        c
              n=0
              do while(.true.)
                 read(*,*,err=1,end=1)x,j
                 new = .true.
                 do i = n,1,-1
                    if (abs(xa(i,3)-x(3)) .gt. 20.0 ) goto 3
                    do k = 1,2
                       if (abs(x(k)-xa(i,k)) .gt. 6.0) goto 2
                    enddo
                    new = .false.
                    xa(i,:)=(xa(i,:)*ja(i)+x*j)/(ja(i)+j)
                    ja(i)=ja(i)+j
          2         continue
                 enddo
          3       if (new) then
                    n=n+1
                    xa(n,:)=x
                    ja(n)=j
                 endif
              enddo
          1   continue
              do i=1,n
                 write(*,*)xa(i,:), ja(i)
              enddo
              end
        """
        listSpotXds = []
        n = 0
        for dozorSpotFile in listDozorSpotFile:
            # Read the file
            with open(str(dozorSpotFile)) as f:
                dozorLines = f.readlines()
            omega = float(dozorLines[2].split()[1]) % 360
            frame = int((omega - oscRange / 2) / oscRange) + 1
            print(omega, frame)
            for dozorLine in dozorLines[3:]:
                new = True
                listValues = dozorLine.split()
                n, xPos, yPos, intensity, sigma = list(map(float, listValues))
                # Subtracting 1 from X and Y: this is because for dozor the upper left pixel in the image is (1,1),
                # whereas for the rest of the world it is (0,0)
                xPos = xPos - 1
                yPos = yPos - 1
                index = 0
                for spotXds in listSpotXds:
                    frameOld = spotXds[2]
                    if abs(frameOld - frame) > 20:
                        break
                    xPosOld = spotXds[0]
                    yPosOld = spotXds[1]
                    intensityOld = spotXds[3]
                    if abs(xPosOld - xPos) <= 6 and abs(yPosOld - yPos) <= 6:
                        new = False
                        intensityNew = intensity + intensityOld
                        xPosNew = (
                            xPosOld * intensityOld + xPos * intensity
                        ) / intensityNew
                        yPosNew = (
                            yPosOld * intensityOld + yPos * intensity
                        ) / intensityNew
                        listSpotXds[index] = [xPosNew, yPosNew, frameOld, intensityNew]
                    index += 1

                if new:
                    spotXds = [xPos, yPos, frame, intensity]
                    listSpotXds.append(spotXds)

        strSpotXds = ""
        for spotXds in listSpotXds:
            strSpotXds += "{0:13.6f}{1:17.6f}{2:17.8f}{3:17.6f}    \n".format(*spotXds)
        return strSpotXds

    @staticmethod
    def writeSPOT_XDS(listDozorSpotFile, oscRange, workingDirectory):
        spotXds = XDSTask.createSPOT_XDS(listDozorSpotFile, oscRange)
        filePath = workingDirectory / "SPOT.XDS"
        with open(str(filePath), "w") as f:
            f.write(spotXds)

    def writeXDS_INP(self, listXDS_INP, workingDirectory):
        fileName = "XDS.INP"
        filePath = workingDirectory / fileName
        with open(str(filePath), "w") as f:
            for line in listXDS_INP:
                f.write(line + "\n")

    @staticmethod
    def getXDSDetector(detector_type):
        untrustedRectangle = []
        nx = UtilsDetector.getNx(detector_type)
        ny = UtilsDetector.getNy(detector_type)
        pixel = UtilsDetector.getPixelsize(detector_type)
        if detector_type == "pilatus2m":
            untrustedRectangle = [
                [487, 495, 0, 1680],
                [981, 989, 0, 1680],
                [0, 1476, 195, 213],
                [0, 1476, 407, 425],
                [0, 1476, 619, 637],
                [0, 1476, 831, 849],
                [0, 1476, 1043, 1061],
                [0, 1476, 1255, 1273],
                [0, 1476, 1467, 1485],
            ]
            sensorThickness = 0.32
        elif detector_type == "pilatus6m":
            untrustedRectangle = [
                [487, 495, 0, 2528],
                [981, 989, 0, 2528],
                [1475, 1483, 0, 2528],
                [1969, 1977, 0, 2528],
                [0, 2464, 195, 213],
                [0, 2464, 407, 425],
                [0, 2464, 619, 637],
                [0, 2464, 831, 849],
                [0, 2464, 1043, 1061],
                [0, 2464, 1255, 1273],
                [0, 2464, 1467, 1485],
                [0, 2464, 1679, 1697],
                [0, 2464, 1891, 1909],
                [0, 2464, 2103, 2121],
                [0, 2464, 2315, 2333],
            ]
            sensorThickness = 0.32
        elif detector_type == "eiger4m":
            untrustedRectangle = [
                [1029, 1040, 0, 2167],
                [0, 2070, 512, 550],
                [0, 2070, 1063, 1103],
                [0, 2070, 1614, 1654],
            ]
            sensorThickness = 0.32
        elif detector_type == "eiger9m":
            untrustedRectangle = [
                [1029, 1040, 0, 3269],
                [2069, 2082, 0, 3269],
                [0, 3110, 513, 553],
                [0, 3110, 1064, 1104],
                [0, 3110, 1615, 1655],
                [0, 3110, 2166, 2206],
                [0, 3110, 2717, 2757],
            ]
        elif detector_type == "eiger16m":
            untrustedRectangle = [
                [0, 4149, 512, 549],
                [0, 4149, 1062, 1099],
                [0, 4149, 1612, 1649],
                [0, 4149, 2162, 2199],
                [0, 4149, 2712, 2749],
                [0, 4149, 3262, 3299],
                [0, 4149, 3812, 3849],
                [513, 514, 0, 4362],
                [1028, 1039, 0, 4362],
                [1553, 1554, 0, 4362],
                [2068, 2079, 0, 4362],
                [2593, 2594, 0, 4362],
                [3108, 3119, 0, 4362],
                [3633, 3634, 0, 4362],
            ]
            sensorThickness = 0.75
        elif detector_type == "pilatus4_4m":
            untrustedRectangle = [
                [0, 2072, 255, 274],
                [0, 2072, 530, 549],
                [0, 2072, 805, 824],
                [0, 2072, 1080, 1099],
                [0, 2072, 1355, 1374],
                [0, 2072, 1630, 1649],
                [0, 2072, 1905, 1924],
                [513, 519, 0, 2179],
                [1033, 1039, 0, 2179],
                [1553, 1559, 0, 2179],
            ]
            sensorThickness = 0.450
        else:
            raise RuntimeError("Unknown detector: {0}".format(detector_type))
        dict_xds_detector = {
            "name": "PILATUS",
            "nx": nx,
            "ny": ny,
            "pixel": pixel,
            "untrustedRectangle": untrustedRectangle,
            "trustedRegion": [0.0, 1.41],
            "trustedpixel": [7000, 30000],
            "minimumValidPixelValue": 0,
            "overload": 1048500,
            "sensorThickness": sensorThickness,
        }
        return dict_xds_detector


class XDSIndexing(XDSTask):
    def generateXDS_INP(self, inData):
        list_xds_inp = XDSTask.generateXDS_INP(inData)
        list_xds_inp.insert(0, "JOB= XYCORR INIT COLSPOT IDXREF")
        # dict_image_links = self.generateImageLinks(inData, self.getWorkingDirectory())
        # list_xds_inp.append(
        #     "NAME_TEMPLATE_OF_DATA_FRAMES= {0}".format(dict_image_links["template"])
        # )
        # list_spot_range = dict_image_links["spotRange"]
        # for spot_range_min, spot_range_max in list_spot_range:
        #     list_xds_inp.append(
        #         "SPOT_RANGE= {0} {1}".format(spot_range_min, spot_range_max)
        #     )
        # list_xds_inp.append(
        #     "DATA_RANGE= {0} {1}".format(
        #         dict_image_links["dataRange"][0], dict_image_links["dataRange"][1]
        #     )
        # )
        # list_spot_range = dict_image_links["excludeDataRange"]
        # for exclude_range_min, exclude_range_max in list_spot_range:
        #     list_xds_inp.append(
        #         "EXCLUDE_DATA_RANGE= {0} {1}".format(
        #             exclude_range_min, exclude_range_max
        #         )
        #     )
        return list_xds_inp

    @staticmethod
    def parseXDSOutput(workingDirectory):
        out_data = None
        idxref_path = workingDirectory / "IDXREF.LP"
        xparm_path = workingDirectory / "XPARM.XDS"
        spot_path = workingDirectory / "SPOT.XDS"
        idxref = XDSIndexing.readIdxrefLp(idxref_path)
        if idxref is not None:
            out_data = {
                "idxref": idxref,
                "xparm": XDSIndexing.parseXparm(xparm_path),
                "xparmXdsPath": xparm_path,
                "spotXdsPath": spot_path,
            }
        return out_data

    @staticmethod
    def parseParameters(indexLine, listLines, resultXDSIndexing):
        if "MOSAICITY" in listLines[indexLine]:
            resultXDSIndexing["mosaicity"] = float(listLines[indexLine].split()[-1])
        elif "DETECTOR COORDINATES (PIXELS) OF DIRECT BEAM" in listLines[indexLine]:
            resultXDSIndexing["xBeam"] = float(listLines[indexLine].split()[-1])
            resultXDSIndexing["yBeam"] = float(listLines[indexLine].split()[-2])
        elif "CRYSTAL TO DETECTOR DISTANCE" in listLines[indexLine]:
            resultXDSIndexing["distance"] = float(listLines[indexLine].split()[-1])

    @staticmethod
    def parseLattice(indexLine, listLines, resultXDSIndexing):
        if listLines[indexLine].startswith(" * ") and not listLines[
            indexLine + 1
        ].startswith(" * "):
            listLine = listLines[indexLine].split()
            latticeCharacter = int(listLine[1])
            bravaisLattice = listLine[2]
            spaceGroup = UtilsSymmetry.getMinimumSymmetrySpaceGroupFromBravaisLattice(
                bravaisLattice
            )
            spaceGroupNumber = UtilsSymmetry.getITNumberFromSpaceGroupName(spaceGroup)
            qualityOfFit = float(listLine[3])
            resultXDSIndexing.update(
                {
                    "latticeCharacter": latticeCharacter,
                    "spaceGroupNumber": spaceGroupNumber,
                    "qualityOfFit": qualityOfFit,
                    "a": float(listLine[4]),
                    "b": float(listLine[5]),
                    "c": float(listLine[6]),
                    "alpha": float(listLine[7]),
                    "beta": float(listLine[8]),
                    "gamma": float(listLine[9]),
                }
            )

    @staticmethod
    def readIdxrefLp(pathToIdxrefLp, resultXDSIndexing=None):
        if resultXDSIndexing is None:
            resultXDSIndexing = {}
        if pathToIdxrefLp.exists():
            with open(str(pathToIdxrefLp)) as f:
                listLines = f.readlines()
            index_line = 0
            do_parse_parameters = False
            do_parse_lattice = False
            while index_line < len(listLines):
                if "!!! ERROR !!!" in listLines[index_line]:
                    resultXDSIndexing = None
                    break
                if (
                    "DIFFRACTION PARAMETERS USED AT START OF INTEGRATION"
                    in listLines[index_line]
                ):
                    do_parse_parameters = True
                    do_parse_lattice = False
                elif (
                    "DETERMINATION OF LATTICE CHARACTER AND BRAVAIS LATTICE"
                    in listLines[index_line]
                ):
                    do_parse_parameters = False
                    do_parse_lattice = True
                if do_parse_parameters:
                    XDSIndexing.parseParameters(
                        index_line, listLines, resultXDSIndexing
                    )
                elif do_parse_lattice:
                    XDSIndexing.parseLattice(index_line, listLines, resultXDSIndexing)
                index_line += 1
        return resultXDSIndexing

    @staticmethod
    def volum(cell):
        """
        Calculate the cell volum from either:
         - the 6 standard cell parameters (a, b, c, alpha, beta, gamma)
         - or the 3 vectors A, B, C
        Inspired from XOconv written by Pierre Legrand:
        https://github.com/legrandp/xdsme/blob/67001a75f3c363bfe19b8bd7cae999f4fb9ad49d/XOconv/XOconv.py#L758
        """
        if len(cell) == 6 and isinstance(cell[0], float):
            # expect a, b, c, alpha, beta, gamma (angles in degree).
            ca, cb, cg = map(XDSIndexing.cosd, cell[3:6])
            return (
                cell[0]
                * cell[1]
                * cell[2]
                * (1 - ca**2 - cb**2 - cg**2 + 2 * ca * cb * cg) ** 0.5
            )
        elif len(cell) == 3 and isinstance(cell[0], np.array):
            # expect vectors of the 3 cell parameters
            A, B, C = cell
            return A * B.cross(C)
        else:
            return "Can't parse input arguments."

    @staticmethod
    def cosd(a):
        return math.cos(a / R2D)

    @staticmethod
    def sind(a):
        return math.sin(a / R2D)

    @staticmethod
    def reciprocal(cell):
        """
        Calculate the 6 reciprocal cell parameters: a*, b*, c*, alpha*, beta*...
        Inspired from XOconv written by Pierre Legrand:
        https://github.com/legrandp/xdsme/blob/67001a75f3c363bfe19b8bd7cae999f4fb9ad49d/XOconv/XOconv.py#L776
        """
        sa, sb, sg = map(XDSIndexing.sind, cell[3:6])
        ca, cb, cg = map(XDSIndexing.cosd, cell[3:6])
        v = XDSIndexing.volum(cell)
        rc = (
            cell[1] * cell[2] * sa / v,
            cell[2] * cell[0] * sb / v,
            cell[0] * cell[1] * sg / v,
            math.acos((cb * cg - ca) / (sb * sg)) * R2D,
            math.acos((ca * cg - cb) / (sa * sg)) * R2D,
            math.acos((ca * cb - cg) / (sa * sb)) * R2D,
        )
        return rc

    @staticmethod
    def BusingLevy(rcell):
        """
        Inspired from XOconv written by Pierre Legrand:
        https://github.com/legrandp/xdsme/blob/67001a75f3c363bfe19b8bd7cae999f4fb9ad49d/XOconv/XOconv.py#L816
        """
        ex = np.array([1, 0, 0])
        ey = np.array([0, 1, 0])
        cosr = list(map(XDSIndexing.cosd, rcell[3:6]))
        sinr = list(map(XDSIndexing.sind, rcell[3:6]))
        Vr = XDSIndexing.volum(rcell)
        BX = ex * rcell[0]
        BY = rcell[1] * (ex * cosr[2] + ey * sinr[2])
        c = rcell[0] * rcell[1] * sinr[2] / Vr
        cosAlpha = (cosr[1] * cosr[2] - cosr[0]) / (sinr[1] * sinr[2])
        BZ = np.array([rcell[2] * cosr[1], -1 * rcell[2] * sinr[1] * cosAlpha, 1 / c])
        return np.array([BX, BY, BZ]).transpose()

    @staticmethod
    def parseXparm(pathToXparmXds):
        """
        Inspired from parse_xparm written by Pierre Legrand:
        https://github.com/legrandp/xdsme/blob/67001a75f3c363bfe19b8bd7cae999f4fb9ad49d/XOconv/XOconv.py#L372
        """
        if pathToXparmXds.exists():
            with open(str(pathToXparmXds)) as f:
                xparm = f.readlines()
            xparamDict = {
                "rot": list(map(float, xparm[1].split()[3:])),
                "beam": list(map(float, xparm[2].split()[1:])),
                "distance": float(xparm[8].split()[2]),
                "originXDS": list(map(float, xparm[8].split()[:2])),
                "A": list(map(float, xparm[4].split())),
                "B": list(map(float, xparm[5].split())),
                "C": list(map(float, xparm[6].split())),
                "cell": list(map(float, xparm[3].split()[1:])),
                "pixel_size": list(map(float, xparm[7].split()[3:])),
                "pixel_numb": list(map(float, xparm[7].split()[1:])),
                "symmetry": int(xparm[3].split()[0]),
                "num_init": list(map(float, xparm[1].split()[:3]))[0],
                "phi_init": list(map(float, xparm[1].split()[:3]))[1],
                "delta_phi": list(map(float, xparm[1].split()[:3]))[2],
                "detector_X": list(map(float, xparm[9].split())),
                "detector_Y": list(map(float, xparm[10].split())),
            }
        else:
            xparamDict = {}
        return xparamDict


class XDSGenerateBackground(XDSTask):
    def generateXDS_INP(self, inData):
        listXDS_INP = XDSTask.generateXDS_INP(inData)
        listXDS_INP.insert(0, "JOB= XYCORR INIT COLSPOT")
        dictImageLinks = self.generateImageLinks(inData, self.getWorkingDirectory())
        listXDS_INP.append(
            "NAME_TEMPLATE_OF_DATA_FRAMES= {0}".format(dictImageLinks["template"])
        )
        listXDS_INP.append(
            "DATA_RANGE= {0} {1}".format(
                dictImageLinks["dataRange"][0], dictImageLinks["dataRange"][1]
            )
        )
        for exclude_data_range in dictImageLinks["excludeDataRange"]:
            listXDS_INP.append(
                "EXCLUDE_DATA_RANGE= {0} {1}".format(
                    exclude_data_range[0], exclude_data_range[1]
                )
            )
        return listXDS_INP

    @staticmethod
    def parseXDSOutput(workingDirectory):
        if (workingDirectory / "BKGINIT.cbf").exists():
            outData = {
                "gainCbf": str(workingDirectory / "GAIN.cbf"),
                "blankCbf": str(workingDirectory / "BLANK.cbf"),
                "bkginitCbf": str(workingDirectory / "BKGINIT.cbf"),
                "xCorrectionsCbf": str(workingDirectory / "X-CORRECTIONS.cbf"),
                "yCorrectionsCbf": str(workingDirectory / "Y-CORRECTIONS.cbf"),
            }
        else:
            outData = {}
        return outData


class XDSIntegration(XDSTask):
    def generateXDS_INP(self, inData):
        # Copy XPARM.XDS, GAIN.CBF file
        shutil.copy(inData["xparmXds"], self.getWorkingDirectory())
        shutil.copy(inData["gainCbf"], self.getWorkingDirectory())
        shutil.copy(inData["xCorrectionsCbf"], self.getWorkingDirectory())
        shutil.copy(inData["yCorrectionsCbf"], self.getWorkingDirectory())
        shutil.copy(inData["blankCbf"], self.getWorkingDirectory())
        shutil.copy(inData["bkginitCbf"], self.getWorkingDirectory())
        listXDS_INP = XDSTask.generateXDS_INP(inData)
        listXDS_INP.insert(0, "JOB= DEFPIX INTEGRATE CORRECT")
        dictImageLinks = self.generateImageLinks(inData, self.getWorkingDirectory())
        listXDS_INP.append(
            "NAME_TEMPLATE_OF_DATA_FRAMES= {0}".format(dictImageLinks["template"])
        )
        listXDS_INP.append(
            "DATA_RANGE= {0} {1}".format(
                dictImageLinks["dataRange"][0], dictImageLinks["dataRange"][1]
            )
        )
        return listXDS_INP

    @staticmethod
    def parseXDSOutput(workingDirectory):
        outData = {}
        if (workingDirectory / "XDS_ASCII.HKL").exists():
            outData = {
                "xdsAsciiHkl": str(workingDirectory / "XDS_ASCII.HKL"),
                "correctLp": str(workingDirectory / "CORRECT.LP"),
                "bkgpixCbf": str(workingDirectory / "BKGPIX.cbf"),
            }
        return outData


class XDSIndexAndIntegration(XDSTask):
    def generateXDS_INP(self, inData):
        listXDS_INP = XDSTask.generateXDS_INP(inData)
        listXDS_INP.insert(
            0, "JOB= XYCORR INIT IDXREF COLSPOT DEFPIX INTEGRATE CORRECT"
        )
        dictImageLinks = self.generateImageLinks(inData, self.getWorkingDirectory())
        listXDS_INP.append(
            "NAME_TEMPLATE_OF_DATA_FRAMES= {0}".format(dictImageLinks["template"])
        )
        no_background_images = min(
            (dictImageLinks["dataRange"][1] - dictImageLinks["dataRange"][0]), 4
        )
        listXDS_INP.append(
            "BACKGROUND_RANGE= {0} {1}".format(
                dictImageLinks["dataRange"][0],
                dictImageLinks["dataRange"][0] + no_background_images - 1,
            )
        )
        listXDS_INP.append(
            "SPOT_RANGE= {0} {1}".format(
                dictImageLinks["dataRange"][0], dictImageLinks["dataRange"][1]
            )
        )
        listXDS_INP.append(
            "DATA_RANGE= {0} {1}".format(
                dictImageLinks["dataRange"][0], dictImageLinks["dataRange"][1]
            )
        )
        return listXDS_INP

    @staticmethod
    def parseXDSOutput(workingDirectory):
        outData = {}
        if (workingDirectory / "XDS_ASCII.HKL").exists():
            outData = {
                "xdsAsciiHkl": str(workingDirectory / "XDS_ASCII.HKL"),
                "correctLp": str(workingDirectory / "CORRECT.LP"),
                "bkgpixCbf": str(workingDirectory / "BKGPIX.cbf"),
            }
        return outData
