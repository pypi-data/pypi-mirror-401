import edna2
import pytest


from edna2.utils import UtilsTest

from edna2.tasks.ControlDozor import ControlDozor


@pytest.mark.skipif(
    not edna2.config.get_site().lower().startswith("esrf"),
    reason="ControlDozor execution test disabled when using non-ESRF config",
)
def test_execute_ControlDozor_eiger16m():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    reference_data_path = data_path / "ControlDozor_eiger16m.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    control_dozor = ControlDozor(inData=in_data)
    control_dozor.execute()
    assert control_dozor.isSuccess()
    out_data = control_dozor.outData
    assert len(out_data["imageQualityIndicators"]) == 4
