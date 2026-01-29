import os
import pathlib
import tempfile

from edna2.utils import UtilsTest

from edna2.tasks.MosflmTasks import AbstractMosflmTask
from edna2.tasks.MosflmTasks import MosflmIndexingTask
from edna2.tasks.MosflmTasks import MosflmGeneratePredictionTask


def test_generateMOSFLMCommands():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    old_edna2_config = os.environ.get("EDNA2_CONFIG", None)
    old_edna2_site = os.environ.get("EDNA2_SITE", None)
    os.environ["EDNA2_CONFIG"] = str(data_path)
    os.environ["EDNA2_SITE"] = "mosflm_testconfig"
    tmpdir = tempfile.mkdtemp(prefix="generateMOSFLMCommands_test_")
    tmp_working_dir = pathlib.Path(tmpdir)
    reference_data_path = data_path / "mosflm_abstract_input.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    abstract_mosflm_task = AbstractMosflmTask(inData=in_data)
    list_commands = abstract_mosflm_task.generateMOSFLMCommands(
        in_data, tmp_working_dir
    )
    # logger.info(pprint.pformat(listCommands))
    for required_item in [
        "BEAM",
        "DETECTOR",
        "OMEGA",
        "REVERSEPHI",
        "DIRECTORY",
        "TEMPLATE",
        "LIMITS EXCLUDE",
        "RASTER",
        "POLARIZATION",
    ]:
        assert required_item in " ".join(list_commands)
    if old_edna2_config:
        os.environ["EDNA2_CONFIG"] = old_edna2_config
    else:
        del os.environ["EDNA2_CONFIG"]
    if old_edna2_site:
        os.environ["EDNA2_SITE"] = old_edna2_site
    else:
        del os.environ["EDNA2_SITE"]


def test_getNewmat():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    newmat = AbstractMosflmTask.getNewmat(data_path / "newmat.txt")
    assert "cell" in newmat
    assert "matrixA" in newmat
    assert "matrixU" in newmat
    assert "missettingsAngles" in newmat


def test_writeNewmat(tmpdir):
    data_path = UtilsTest.prepareTestDataPath(__file__)
    newmat_json_path = data_path / "newmat.json"
    newmat = UtilsTest.loadAndSubstitueTestData(newmat_json_path)
    newmat_path = pathlib.Path(tmpdir) / "newmat.txt"
    AbstractMosflmTask.writeNewmat(newmat, newmat_path)
    assert newmat_path.exists()


def test_generateMOSFLMCommands_indexing(tmpdir):
    data_path = UtilsTest.prepareTestDataPath(__file__)
    old_edna2_config = os.environ.get("EDNA2_CONFIG", None)
    old_edna2_site = os.environ.get("EDNA2_SITE", None)
    os.environ["EDNA2_CONFIG"] = str(data_path)
    os.environ["EDNA2_SITE"] = "mosflm_testconfig"
    tmp_working_dir = pathlib.Path(tmpdir)
    reference_data_path = data_path / "mosflm_abstract_input.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    task = MosflmIndexingTask(in_data)
    list_commands = task.generateMOSFLMCommands(in_data, tmp_working_dir)
    for required_item in [
        "BEAM",
        "DETECTOR",
        "OMEGA",
        "REVERSEPHI",
        "DIRECTORY",
        "TEMPLATE",
        "LIMITS EXCLUDE",
        "RASTER",
        "POLARIZATION",
    ]:
        assert required_item in " ".join(list_commands)
    if old_edna2_config:
        os.environ["EDNA2_CONFIG"] = old_edna2_config
    else:
        del os.environ["EDNA2_CONFIG"]
    if old_edna2_site:
        os.environ["EDNA2_SITE"] = old_edna2_site
    else:
        del os.environ["EDNA2_SITE"]


def test_parseIndexingMosflmOutput():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    new_mat_file_path = data_path / "newmat.txt"
    dna_tables_path = data_path / "indexingTwoImagesDnaTables.xml"
    task = MosflmIndexingTask(inData={})
    out_data = task.parseIndexingMosflmOutput(new_mat_file_path, dna_tables_path)
    for parameter in [
        "newmat",
        "mosaicityEstimation",
        "deviationAngular",
        "refinedDistance",
        "spotsUsed",
        "spotsTotal",
        "selectedSolutionNumber",
        "selectedSolutionSpaceGroup",
        "selectedSolutionSpaceGroupNumber",
        "indexingSolution",
    ]:
        assert parameter in out_data, parameter


def test_generateMOSFLMCommands_generatePrediction(tmpdir):
    data_path = UtilsTest.prepareTestDataPath(__file__)
    reference_data_path = data_path / "mosflm_generatePrediction_2m_RNASE_1.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    task = MosflmGeneratePredictionTask(in_data)
    list_commands = task.generateMOSFLMCommands(in_data, tmpdir)
    for command in [
        "WAVELENGTH 0.8729",
        "DISTANCE 305.222",
        "BEAM 113.5544 112.2936",
        "TEMPLATE ref-2m_RNASE_1_####.cbf",
        "SYMMETRY P1",
        "EXIT",
    ]:
        assert command in list_commands
