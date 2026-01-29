import pytest

import edna2.config

from edna2.utils import UtilsTest

from edna2.tasks.MosflmTasks import MosflmGeneratePredictionTask


@pytest.mark.skipif(
    True,
    reason="Disabled",
)
def test_execute_MosflmGeneratePredictionTask_2m_RNASE_1(self):
    data_path = UtilsTest.prepareTestDataPath(__file__)
    UtilsTest.loadTestImage("ref-2m_RNASE_1_0001.cbf")
    UtilsTest.loadTestImage("ref-2m_RNASE_1_0002.cbf")
    reference_data_path = data_path / "mosflm_generatePrediction_2m_RNASE_1.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    mosflm_indexing_task = MosflmGeneratePredictionTask(inData=in_data)
    mosflm_indexing_task.execute()
    assert mosflm_indexing_task.isSuccess()


@pytest.mark.skipif(
    edna2.config.get_site() == "Default",
    reason="Cannot run mosflm test with default config",
)
def test_execute_MosflmGeneratePredictionTaskTRYP_X1_4():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    UtilsTest.loadTestImage("ref-TRYP-X1_4_0001.cbf")
    UtilsTest.loadTestImage("ref-TRYP-X1_4_0002.cbf")
    UtilsTest.loadTestImage("ref-TRYP-X1_4_0003.cbf")
    UtilsTest.loadTestImage("ref-TRYP-X1_4_0004.cbf")
    reference_data_path = data_path / "mosflm_generatePrediction_TRYP-X1_4.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    mosflm_indexing_task = MosflmGeneratePredictionTask(inData=in_data)
    mosflm_indexing_task.execute()
    assert mosflm_indexing_task.isSuccess()
