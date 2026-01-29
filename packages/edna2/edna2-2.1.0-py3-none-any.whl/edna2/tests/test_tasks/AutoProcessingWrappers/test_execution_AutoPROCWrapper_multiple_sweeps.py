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
@pytest.mark.skipif(
    not os.path.exists(
        "/data/scisoft/pxsoft/data/WORKFLOW_TEST_DATA/id30a1/20250828/RAW_DATA/CHEM2/CHEM2-CHEM2-A037-c02e14-005/run_01_MXPressA/run_01_08_datacollection"
    ),
    reason="Test data not present",
)
def test_execute_multiple_sweeps():
    in_data = {
        "start_image_number": 1,
        "end_image_number": 50,
        "raw_data": [
            "/data/scisoft/pxsoft/data/WORKFLOW_TEST_DATA/id30a1/20250828/RAW_DATA/CHEM2/CHEM2-CHEM2-A037-c02e14-005/run_01_MXPressA/run_01_05_datacollection",
            "/data/scisoft/pxsoft/data/WORKFLOW_TEST_DATA/id30a1/20250828/RAW_DATA/CHEM2/CHEM2-CHEM2-A037-c02e14-005/run_01_MXPressA/run_01_08_datacollection",
        ],
    }
    autoProcessingWrappers = AutoPROCWrapper(inData=in_data)
    autoProcessingWrappers.execute()
    out_data = autoProcessingWrappers.outData
    assert out_data is not None
