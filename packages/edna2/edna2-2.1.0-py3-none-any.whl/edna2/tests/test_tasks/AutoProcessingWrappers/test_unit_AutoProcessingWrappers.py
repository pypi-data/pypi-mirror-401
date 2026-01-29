import pytest

from edna2 import config

from edna2.utils import UtilsTest

from edna2.tasks.AutoProcessingWrappers import AutoPROCWrapper


def get_ispyb_xml():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    auto_proc_xml_path = data_path / "autoPROC.xml"
    with open(auto_proc_xml_path) as f:
        ispyb_xml = f.read()
    return ispyb_xml


def test_create_icat_metadata_from_ispyb_xml():
    ispyb_xml = get_ispyb_xml()
    icat_metadata = AutoPROCWrapper.create_icat_metadata_from_ispyb_xml(ispyb_xml)
    assert icat_metadata is not None


@pytest.mark.skipif(
    not config.get_site().lower().startswith("esrf"),
    reason="AutoPROCWrapper.get_metadata test disabled when using non-ESRF config",
)
def test_get_metadata():
    raw_data_path = "/data/scisoft/pxsoft/data/WORKFLOW_TEST_DATA/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_07_datacollection"
    metadata = AutoPROCWrapper.get_metadata(raw_data_path)
    assert metadata is not None


@pytest.mark.skipif(
    not config.get_site().lower().startswith("esrf"),
    reason="AutoPROCWrapper.wait_for_data test disabled when using non-ESRF config",
)
def test_wait_for_data_cbf():
    in_data = {
        "raw_data": [
            "/data/scisoft/pxsoft/data/WORKFLOW_TEST_DATA/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_07_datacollection",
            "/data/scisoft/pxsoft/data/WORKFLOW_TEST_DATA/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_09_datacollection",
            "/data/scisoft/pxsoft/data/WORKFLOW_TEST_DATA/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_11_datacollection",
            "/data/scisoft/pxsoft/data/WORKFLOW_TEST_DATA/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_13_datacollection",
        ]
    }
    is_success = AutoPROCWrapper.wait_for_data(in_data)
    assert is_success
