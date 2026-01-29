import os
import pytest
import edna2.config

from edna2.utils import UtilsTest

from edna2.tasks.XDSTasks import XDSGenerateBackground


@pytest.mark.skipif(
    True,
    reason="Disabled during XDS tasks refactoring",
)
@pytest.mark.skipif(
    not edna2.config.get_site().lower().startswith("esrf"),
    reason="XDS execution test disabled when using non-ESRF config",
)
def test_execute_XDSGenerateBackground():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    reference_data_path = data_path / "inDataXDSGenerateBackground.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    xds_generate_background = XDSGenerateBackground(inData=in_data)
    xds_generate_background.execute()
    assert xds_generate_background.isSuccess()
    backgroundImage = xds_generate_background.outData["bkginitCbf"]
    assert os.path.exists(backgroundImage)
