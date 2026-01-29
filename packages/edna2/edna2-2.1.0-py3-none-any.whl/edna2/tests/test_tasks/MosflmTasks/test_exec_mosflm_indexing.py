import pytest

import edna2.config

from edna2.utils import UtilsTest

from edna2.tasks.MosflmTasks import MosflmIndexingTask


@pytest.mark.skipif(
    edna2.config.get_site() == "Default",
    reason="Cannot run mosflm test with default config",
)
def test_execute_mosflm_indexing_task_TRYP_X1_4():
    dataPath = UtilsTest.prepareTestDataPath(__file__)
    UtilsTest.loadTestImage("ref-TRYP-X1_4_0001.cbf")
    UtilsTest.loadTestImage("ref-TRYP-X1_4_0002.cbf")
    UtilsTest.loadTestImage("ref-TRYP-X1_4_0003.cbf")
    UtilsTest.loadTestImage("ref-TRYP-X1_4_0004.cbf")
    reference_data_path = dataPath / "mosflm_indexing_TRYP-X1_4.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    mosflm_indexing_task = MosflmIndexingTask(inData=in_data)
    mosflm_indexing_task.execute()
    assert mosflm_indexing_task.isSuccess()


@pytest.mark.skipif(
    edna2.config.get_site() == "Default",
    reason="Cannot run mosflm test with default config",
)
def test_execute_mosflm_indexing_task_TRYP_X1_4_2():
    dataPath = UtilsTest.prepareTestDataPath(__file__)
    reference_data_path = dataPath / "TRYP-X1_4.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    mosflm_indexing_task = MosflmIndexingTask(inData=in_data)
    mosflm_indexing_task.execute()
    assert mosflm_indexing_task.isSuccess()


@pytest.mark.skipif(
    edna2.config.get_site() == "Default",
    reason="Cannot run mosflm test with default config",
)
def test_execute_mosflm_indexing_task_fae_3():
    dataPath = UtilsTest.prepareTestDataPath(__file__)
    UtilsTest.loadTestImage("ref-fae_3_0001.h5")
    UtilsTest.loadTestImage("ref-fae_3_0002.h5")
    UtilsTest.loadTestImage("ref-fae_3_0003.h5")
    UtilsTest.loadTestImage("ref-fae_3_0004.h5")
    reference_data_path = dataPath / "mosflm_indexing_fae_3.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    mosflm_indexing_task = MosflmIndexingTask(inData=in_data)
    mosflm_indexing_task.execute()
    assert mosflm_indexing_task.isSuccess()


@pytest.mark.skipif(
    True,
    reason="Disabled",
)
def test_aggregate_master():
    import h5py

    filePath = "/opt/pxsoft/bes/vgit/linux-x86_64/id30a2/edna2/testdata/images/ref-fae_3_1_data_000001.h5"
    filePath1 = "/opt/pxsoft/bes/vgit/linux-x86_64/id30a2/edna2/testdata/images/ref-fae_3_1_master.h5"
    filePath2 = "/opt/pxsoft/bes/vgit/linux-x86_64/id30a2/edna2/testdata/images/ref-fae_3_2_master.h5"
    filePath3 = "/opt/pxsoft/bes/vgit/linux-x86_64/id30a2/edna2/testdata/images/ref-fae_3_3_master.h5"
    filePath4 = "/opt/pxsoft/bes/vgit/linux-x86_64/id30a2/edna2/testdata/images/ref-fae_3_4_master.h5"
    f1 = h5py.File(filePath1, "r")
    f2 = h5py.File(filePath2, "r")
    f3 = h5py.File(filePath3, "r")
    f4 = h5py.File(filePath4, "r")
    data1 = f1["entry"]["data"]["data_000001"][()]
    data2 = f2["entry"]["data"]["data_000001"][()]
    data3 = f3["entry"]["data"]["data_000001"][()]
    data4 = f4["entry"]["data"]["data_000001"][()]
    # f.create_group('entry')
    # entry = f['entry']
    # entry.create_group('data')
    # data = entry['data']
    f = h5py.File(filePath, "w")
    data_000001 = f.create_dataset("/entry/data/data", (4, 4362, 4148), dtype="uint32")
    data_000001[0, :, :] = data1[0, :, :]
    data_000001[1, :, :] = data2[0, :, :]
    data_000001[2, :, :] = data3[0, :, :]
    data_000001[3, :, :] = data4[0, :, :]
    # data['data_000001'] = data_000001
    # pprint.pprint(data.keys())
    # pprint.pprint(data.values())
    f.close()


@pytest.mark.skipif(
    True,
    reason="Disabled",
)
def test_modify_master():
    import h5py

    filePath1 = "/opt/pxsoft/bes/vgit/linux-x86_64/id30a2/edna2/testdata/images/ref-fae_3_1_master.h5"
    f1 = h5py.File(filePath1, "r+")
    entry = f1["entry"]
    nimages = entry["instrument"]["detector"]["detectorSpecific"]["nimages"]
    print(dir(nimages))
    entry["instrument"]["detector"]["detectorSpecific"]["nimages"][()] = 4
    f1.close()
