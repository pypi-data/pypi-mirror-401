import edna2
import pytest

from edna2.utils import UtilsTest

from edna2.tasks.ControlDozor import ControlDozor


@pytest.mark.skipif(
    not edna2.config.get_site().lower().startswith("esrf"),
    reason="ControlDozor execution test disabled when using non-ESRF config",
)
def test_execute_ControlDozor_pilatus4_4m():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    reference_data_path = data_path / "ControlDozor_pilatus4_4m.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    controlDozor = ControlDozor(inData=in_data)
    controlDozor.execute()
    assert controlDozor.isSuccess()
    outData = controlDozor.outData
    assert outData["detectorType"] == "pilatus4_4m"
    assert len(outData["imageQualityIndicators"]) == 1
    assert outData["imageQualityIndicators"][0]["dozorSpotScore"] > 400
