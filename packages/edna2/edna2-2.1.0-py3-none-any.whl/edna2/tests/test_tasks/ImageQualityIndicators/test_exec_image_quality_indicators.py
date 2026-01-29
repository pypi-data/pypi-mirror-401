import os
import pytest

import edna2.config

from edna2.utils import UtilsTest

from edna2.tasks.ImageQualityIndicators import ImageQualityIndicators


@pytest.mark.skipif(
    edna2.config.get_site() == "Default",
    reason="Cannot run ImageQualityIndicatorsExecTest " + "test with default config",
)
@pytest.mark.skipif(
    not os.path.exists(
        "/data/scisoft/pxsoft/data/WORKFLOW_TEST_DATA/id30a2/inhouse/opid30a2"
        + "/20191129/RAW_DATA/t1/MeshScan_05/mesh-t1_1_0001.cbf"
    ),
    reason="Cannot find CBF file mesh-t1_1_0001.cbf",
)
def test_execute():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    reference_data_path = data_path / "inDataImageQualityIndicatorsTask.json"
    inData = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    task = ImageQualityIndicators(inData=inData)
    task.execute()
    assert not task.isFailure()
    out_data = task.outData
    assert "imageQualityIndicators" in out_data
    # assert 'resolution_limit' in out_data['crystfel_results'][0])
    assert 72 == len(out_data["imageQualityIndicators"])
