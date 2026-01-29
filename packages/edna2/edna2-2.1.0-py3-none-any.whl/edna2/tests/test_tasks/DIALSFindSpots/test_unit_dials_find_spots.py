import pytest
import pathlib

from edna2.utils import UtilsTest

from edna2.tasks.DIALSFindSpots import DIALSFindSpots

TEST_MASTER_PATH = (
    "/data/scisoft/pxsoft/data/WORKFLOW_TEST_DATA/id30a1/20250825/RAW_DATA/"
    + "Sample-1-2-01/run_01_MXPressA/run_01_02_mesh/mesh-Sample-1-2-01_1_2_1_master.h5"
)


def test_parseDIALSLogFile():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    dials_log_file = data_path / "dials.find_spots.log"
    list_positions = DIALSFindSpots.parseDIALSLogFile(dials_log_file)
    assert len(list_positions) == 10


@pytest.mark.skipif(
    not pathlib.Path(TEST_MASTER_PATH).exists(),
    reason=f"Cannot run unit test of test_fix_mesh_master_file because test file {TEST_MASTER_PATH} missing",
)
def test_fix_mesh_master_file(tmp_path):
    mesh_master_path = pathlib.Path(TEST_MASTER_PATH)
    new_master_path = tmp_path / "new_master.h5"
    DIALSFindSpots.fix_mesh_master_file(mesh_master_path, new_master_path)
    assert new_master_path.exists()
