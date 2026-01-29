import os
import json
import edna2
import pytest

from edna2.utils import UtilsTest
from edna2.tasks.ControlDozor import ControlDozor


@pytest.mark.skipif(
    not edna2.config.get_site().lower().startswith("esrf"),
    reason="ControlDozor plot test disabled when using non-ESRF config",
)
def test_makePlot(tmpdir):
    data_path = UtilsTest.prepareTestDataPath(__file__)
    data_collection_id = 123456
    out_data_path = data_path / "outDataControlDozor.json"
    with open(str(out_data_path)) as f:
        out_data = json.load(f)
    control_dozor = ControlDozor(inData={})
    control_dozor.template = "mesh-test_1_%4d.cbf"
    control_dozor.directory = UtilsTest.getTestImageDirPath().as_posix()
    dozor_plot_path, dozor_csv_path = control_dozor.makePlot(
        data_collection_id, out_data, tmpdir
    )
    assert os.path.exists(dozor_plot_path)
    assert os.path.exists(dozor_csv_path)
