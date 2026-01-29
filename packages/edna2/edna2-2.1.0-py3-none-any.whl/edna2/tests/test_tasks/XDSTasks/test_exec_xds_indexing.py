import pytest

import edna2.config

from edna2.utils import UtilsTest

from edna2.tasks.XDSTasks import XDSIndexing


@pytest.mark.skipif(
    not edna2.config.get_site().lower().startswith("esrf"),
    reason="XDS execution test disabled when using non-ESRF config",
)
def test_execute_xds_indexing_1():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    reference_data_path = data_path / "indata_xds_indexing_pilatus4_4m_1.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    xds_indexing = XDSIndexing(inData=in_data)
    xds_indexing.execute()
    assert xds_indexing.isSuccess()
    out_data = xds_indexing.outData
    idxref = out_data["idxref"]
    assert idxref
    assert idxref["spaceGroupNumber"] == 75
