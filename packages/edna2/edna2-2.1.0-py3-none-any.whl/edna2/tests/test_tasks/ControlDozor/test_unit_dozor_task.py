import os
import json
import edna2
import pytest

from edna2.tasks.ControlDozor import ExecDozor

from edna2.utils import UtilsTest


@pytest.fixture
def data_path():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    return data_path


@pytest.fixture
def in_data(data_path):
    referenceDataPath = data_path / "inDataDozor.json"
    with open(str(referenceDataPath)) as f:
        in_data = json.load(f)
    return in_data


@pytest.fixture
def exec_dozor(in_data):
    exec_dozor = ExecDozor(inData=in_data)
    return exec_dozor


@pytest.mark.skipif(
    not edna2.config.get_site().lower().startswith("esrf"),
    reason="Dozor test_generateCommands disabled when using non-ESRF config",
)
def test_generateCommands(in_data):
    dozor = ExecDozor(inData=in_data)
    strCommandText = dozor.generateCommands(in_data)
    # print(strCommandText)
    assert strCommandText is not None


def test_parseOutput(in_data, data_path):
    dozor = ExecDozor(inData=in_data)
    dozor.startingAngle = 10.0
    dozor.firstImageNumber = 1
    dozor.oscillationRange = 0.1
    dozor.overlap = 0.0
    log_file_name = data_path / "Dozor_v2.0.2.log"
    with open(str(log_file_name)) as f:
        output = f.read()
    result = dozor.parseOutput(in_data, output, prepareDozorAllFile=False)
    assert len(result["imageDozor"]), "Result from 10 images" == 10
    # Log file with 'no results'
    log_file_name2 = data_path / "Dozor_v2.0.2_no_results.log"
    with open(str(log_file_name2)) as f:
        output2 = f.read()
    result2 = dozor.parseOutput(in_data, output2, prepareDozorAllFile=False)
    assert len(result2["imageDozor"]), "Result from 51 images" == 51


def test_parseDouble():
    assert ExecDozor.parseDouble("1.0") == 1.0
    assert ExecDozor.parseDouble("****") is None


def test_generatePngPlots(tmpdir, data_path):
    plotmtvFile = data_path / "dozor_rd.mtv"
    listFile = ExecDozor.generatePngPlots(plotmtvFile, tmpdir)
    for plotFile in listFile:
        assert os.path.exists(plotFile)


@pytest.mark.skipif(
    not edna2.config.get_site().lower().startswith("esrf"),
    reason="Dozor test_getLibrary disabled when using non-ESRF config",
)
def test_getLibrary(in_data):
    dozor = ExecDozor(inData=in_data)
    library = dozor.getLibrary("cbf")
    assert "xds-zcbf.so" in library
    library = dozor.getLibrary("hdf5")
    assert "dectris-neggia.so" in library
