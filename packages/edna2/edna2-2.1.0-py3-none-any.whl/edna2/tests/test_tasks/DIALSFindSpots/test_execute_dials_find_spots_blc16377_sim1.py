import pytest

from edna2 import config

from edna2.utils import UtilsTest
from edna2.utils import UtilsLogging

from edna2.tasks.DIALSFindSpots import DIALSFindSpots

logger = UtilsLogging.getLogger()


@pytest.mark.skipif(
    not config.get_site().lower().startswith("esrf"),
    reason="DIALSFindSpots exec test disabled when using non-ESRF config",
)
def test_execute_DIALSFindSpots(tmpdir):
    data_path = UtilsTest.prepareTestDataPath(__file__)
    reference_data_path = data_path / "blc16377_sim1.json"
    inData = UtilsTest.loadAndSubstitueTestData(reference_data_path, tmpDir=tmpdir)
    dials_find_spots = DIALSFindSpots(inData=inData)
    dials_find_spots.execute()
    assert dials_find_spots.isSuccess()
    out_data = dials_find_spots.outData
    assert out_data is not None
    list_positions = out_data["listPositions"]
    for position in list_positions:
        assert "totalIntensity" in position
        assert "noSpots" in position
