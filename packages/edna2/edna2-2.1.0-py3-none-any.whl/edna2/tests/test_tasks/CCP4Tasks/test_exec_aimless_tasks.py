import pytest

from edna2 import config

from edna2.utils import UtilsTest
from edna2.utils import UtilsLogging

from edna2.tasks.CCP4Tasks import AimlessTask

logger = UtilsLogging.getLogger()


@pytest.mark.skipif(
    not config.get_site().lower().startswith("esrf"),
    reason="Aimless exec test disabled when using non-ESRF config",
)
def test_execute_AimlessTask(tmpdir):
    data_path = UtilsTest.prepareTestDataPath(__file__)
    reference_data_path = data_path / "inDataAimlessTask.json"
    inData = UtilsTest.loadAndSubstitueTestData(reference_data_path, tmpDir=tmpdir)
    aimlessTask = AimlessTask(inData=inData)
    aimlessTask.execute()
    assert aimlessTask.isSuccess()
    outData = aimlessTask.outData
    assert outData["isSuccess"]
