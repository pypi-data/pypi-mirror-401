import edna2
import pytest

from edna2.utils import UtilsTest

from edna2.tasks.CCP4Tasks import PointlessTask

from edna2.utils import UtilsLogging

logger = UtilsLogging.getLogger()


@pytest.mark.skipif(
    not edna2.config.get_site().lower().startswith("esrf"),
    reason="Pointless exec test disabled when using non-ESRF config",
)
def test_execute_PointlessTask(tmpdir):
    data_path = UtilsTest.prepareTestDataPath(__file__)
    reference_data_path = data_path / "inDataPointlessTask.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path, tmpDir=tmpdir)
    task = PointlessTask(inData=in_data)
    task.execute()
    assert task.isSuccess()
    outData = task.outData
    assert outData["isSuccess"]
