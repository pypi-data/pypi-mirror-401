import pytest
import edna2.config

from edna2.utils import UtilsTest

from edna2.tasks.ControlIndexing import ControlIndexing


@pytest.mark.skipif(
    not edna2.config.get_site().lower().startswith("esrf"),
    reason="ControlIndexing execution test disabled when using non-ESRF config",
)
def test_execute_ControlIndexing_id30a1_gphl():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    reference_data_path = data_path / "id30a1_GPhL_test.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    control_indexing = ControlIndexing(
        inData=in_data, workingDirectorySuffix="local_user_1"
    )
    control_indexing.execute()
    assert control_indexing.isSuccess()
    assert control_indexing.outData["resultIndexing"]["spaceGroupNumber"] == 1
