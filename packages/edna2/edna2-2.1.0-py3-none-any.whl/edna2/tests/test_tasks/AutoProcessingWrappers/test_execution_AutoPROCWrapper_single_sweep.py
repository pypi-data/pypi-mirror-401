import os
import pytest

from edna2 import config

from edna2.tasks.AutoProcessingWrappers import AutoPROCWrapper


@pytest.mark.skipif(
    not config.get_site().lower().startswith("esrf"),
    reason="AutoPROCWrapper exec test disabled when using non-ESRF config",
)
@pytest.mark.skipif(
    not os.path.exists(
        "/data/scisoft/pxsoft/data/WORKFLOW_TEST_DATA/id30a1/20250828/RAW_DATA/CHEM2/CHEM2-CHEM2-A037-c02e14-005/run_01_MXPressA/run_01_05_datacollection"
    ),
    reason="Test data not present",
)
def test_execute_single_sweep():
    in_data = {
        "start_image_number": 1,
        "end_image_number": 50,
        "raw_data": [
            "/data/scisoft/pxsoft/data/WORKFLOW_TEST_DATA/id30a1/20250828/RAW_DATA/CHEM2/CHEM2-CHEM2-A037-c02e14-005/run_01_MXPressA/run_01_05_datacollection",
        ],
    }
    autoProcessingWrappers = AutoPROCWrapper(inData=in_data)
    autoProcessingWrappers.execute()
    out_data = autoProcessingWrappers.outData
    assert out_data is not None


# def tes_upload_autoPROC_to_icat():
#     # tmp_path = pathlib.Path(tmpdir)
#     # ispyb_xml = get_ispyb_xml()
#     # working_dir = tmp_path / "nobackup"
#     os.environ["EDNA2_SITE"] = "ESRF_ID30A1"
#     processed_data_dir = pathlib.Path(
#         "/data/visitor/mx2532/id30a1/20240220/PROCESSED_DATA/INS/INS-Helical_test1/run_01_MXPressA/autoprocessing_combined/autoPROC"
#     )
#     list_raw_dir = [
#         "/data/visitor/mx2532/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_MXPressA/run_01_07_datacollection",
#         "/data/visitor/mx2532/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_MXPressA/run_01_09_datacollection",
#         "/data/visitor/mx2532/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_MXPressA/run_01_11_datacollection",
#         "/data/visitor/mx2532/id30a1/20240220/RAW_DATA/INS/INS-Helical_test1/run_01_MXPressA/run_01_13_datacollection",
#     ]
#     AutoPROCWrapper.upload_autoPROC_to_icat(
#         beamline="id30a1",
#         proposal="mx2532",
#         processName="autoPROC",
#         list_raw_dir=list_raw_dir,
#         processed_data_dir=processed_data_dir,
#     )
