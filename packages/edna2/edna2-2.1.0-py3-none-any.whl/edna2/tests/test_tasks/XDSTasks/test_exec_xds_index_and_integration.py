import pytest

from edna2.utils import UtilsTest

from edna2.tasks.XDSTasks import XDSIndexAndIntegration


@pytest.mark.skipif(
    True,
    reason="XDSIndexAndIntegration disabled due to missing test data",
)
def test_execute_XDSIntegration(self):
    reference_data_path = self.dataPath / "id30a1_1_fast_char.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    xds_index_and_integration = XDSIndexAndIntegration(inData=in_data)
    xds_index_and_integration.execute()
    assert xds_index_and_integration.isSuccess()
