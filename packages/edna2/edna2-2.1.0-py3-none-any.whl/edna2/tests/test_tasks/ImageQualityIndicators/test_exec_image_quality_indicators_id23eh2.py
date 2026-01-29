import pytest
import edna2.config

from edna2.utils import UtilsTest

from edna2.tasks.ImageQualityIndicators import ImageQualityIndicators


@pytest.mark.skipif(
    edna2.config.get_site() == "Default",
    reason="Cannot run ImageQualityIndicatorsExecTest " + "test with default config",
)
@pytest.mark.skipif(True, reason="Disabled")
def test_execute():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    reference_data_path = data_path / "id23eh2.json"
    inData = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    task = ImageQualityIndicators(inData=inData)
    task.execute()
    assert not task.isFailure()
    out_data = task.outData
    assert "imageQualityIndicators" in out_data
    assert 4592 == len(out_data["imageQualityIndicators"])
