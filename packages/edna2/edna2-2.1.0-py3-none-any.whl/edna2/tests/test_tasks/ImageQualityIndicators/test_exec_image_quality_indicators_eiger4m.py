import pytest
import edna2.config

from edna2.utils import UtilsTest

from edna2.tasks.ImageQualityIndicators import ImageQualityIndicators


@pytest.mark.skipif(
    edna2.config.get_site() == "Default",
    reason="Cannot run ImageQualityIndicatorsExecTest " + "test with default config",
)
def test_execute_eiger4m_h5_10images():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    UtilsTest.loadTestImage("mesh-mx415_1_0001.h5")
    reference_data_path = data_path / "eiger4m_h5_10images.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    task = ImageQualityIndicators(inData=in_data)
    task.execute()
    assert not task.isFailure()
    out_data = task.outData
    assert "imageQualityIndicators" in out_data
    assert len(out_data["imageQualityIndicators"]) == 51
    # Check DIALS findspots output
    quality_indicators = out_data["imageQualityIndicators"][50]
    assert "dialsTotalIntensity" in quality_indicators
    assert "dialsNoSpots" in quality_indicators
