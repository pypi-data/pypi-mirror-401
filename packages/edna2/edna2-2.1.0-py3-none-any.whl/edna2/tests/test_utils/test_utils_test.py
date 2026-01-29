import os
import pytest

from edna2.utils import UtilsTest


@pytest.fixture
def indata1():
    return {"image": "$EDNA2_TESTDATA_IMAGES/ref-2m_RNASE_1_0001.cbf"}


@pytest.fixture
def indata2():
    return {
        "images": [
            "$EDNA2_TESTDATA_IMAGES/ref-2m_RNASE_1_0001.cbf",
            "$EDNA2_TESTDATA_IMAGES/ref-2m_RNASE_1_0002.cbf",
        ]
    }


def test_getTestdataPath():
    testdataDir = UtilsTest.getTestdataPath()
    print(testdataDir)


def test_substitute(indata1, indata2):
    # One unix path
    newInData1 = UtilsTest.substitute(indata1, "$EDNA2_TESTDATA_IMAGES", "/data")
    assert newInData1["image"] == "/data/ref-2m_RNASE_1_0001.cbf"
    # Two unix paths
    newInData2 = UtilsTest.substitute(indata2, "$EDNA2_TESTDATA_IMAGES", "/data")
    assert newInData2["images"][0] == "/data/ref-2m_RNASE_1_0001.cbf"
    assert newInData2["images"][1] == "/data/ref-2m_RNASE_1_0002.cbf"


def test_getSearchStringFileNames(indata1, indata2):
    listFileNames1 = UtilsTest.getSearchStringFileNames(
        "$EDNA2_TESTDATA_IMAGES", indata1
    )
    assert listFileNames1 == ["ref-2m_RNASE_1_0001.cbf"]
    listFileNames2 = UtilsTest.getSearchStringFileNames(
        "$EDNA2_TESTDATA_IMAGES", indata2
    )
    assert listFileNames2 == ["ref-2m_RNASE_1_0001.cbf", "ref-2m_RNASE_1_0002.cbf"]


def test_loadTestImages():
    image_file_name = "FAE_1_1_00001.cbf"
    path_image = UtilsTest.getTestImageDirPath() / image_file_name
    if path_image.exists():
        os.remove(str(path_image))
    UtilsTest.loadTestImage(image_file_name)
    assert path_image.exists()
    os.remove(str(path_image))


def test_substitueTestData():
    indata = {"image": "$EDNA2_TESTDATA_IMAGES/ref-2m_RNASE_1_0001.cbf"}
    new_indata = UtilsTest.substitueTestData(indata)
    assert os.path.exists(new_indata["image"])
    os.remove(new_indata["image"])
