import pytest
import edna2.config

from edna2.utils import UtilsTest

from edna2.tasks.XDSTasks import XDSIntegration


@pytest.mark.skipif(
    True,
    reason="Disabled during XDS tasks refactoring",
)
@pytest.mark.skipif(
    not edna2.config.get_site().lower().startswith("esrf"),
    reason="XDS execution test disabled when using non-ESRF config",
)
def test_execute_XDSIntegration():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    reference_data_path = data_path / "inDataXDSIntegration.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    xds_integration = XDSIntegration(inData=in_data)
    xds_integration.execute()
    assert xds_integration.isSuccess()
