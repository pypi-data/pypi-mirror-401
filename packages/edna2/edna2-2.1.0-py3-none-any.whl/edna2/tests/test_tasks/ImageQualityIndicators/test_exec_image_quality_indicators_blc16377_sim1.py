import pytest
import edna2.config

from edna2.utils import UtilsTest

from edna2.tasks.ImageQualityIndicators import ImageQualityIndicators


@pytest.mark.skipif(
    edna2.config.get_site() == "Default",
    reason="Cannot run ImageQualityIndicatorsExecTest " + "test with default config",
)
def test_execute():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    reference_data_path = data_path / "blc16377_sim1.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    task = ImageQualityIndicators(inData=in_data)
    task.execute()
    assert not task.isFailure()
    out_data = task.outData
    assert "imageQualityIndicators" in out_data
    list_indicators = out_data["imageQualityIndicators"]
    for indicators in list_indicators:
        assert "dozorScore" in indicators
        assert "dialsTotalIntensity" in indicators
