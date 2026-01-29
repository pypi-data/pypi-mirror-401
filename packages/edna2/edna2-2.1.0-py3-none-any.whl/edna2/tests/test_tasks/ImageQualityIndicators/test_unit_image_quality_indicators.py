import pathlib


from edna2.tasks.ImageQualityIndicators import ImageQualityIndicators


def testGetH5FilePath():
    filePath1 = pathlib.Path(
        "/data/id30a3/inhouse/opid30a3/20160204/RAW_DATA/"
        + "meshtest/XrayCentering_01/mesh-meshtest_1_0001.cbf"
    )
    (
        h5MasterFilePath1,
        h5DataFilePath1,
        h5FileNumber,
    ) = ImageQualityIndicators.getH5FilePath(filePath1, 9)
    h5MasterFilePath1Reference = pathlib.Path(
        "/data/id30a3/inhouse/opid30a3/20160204/RAW_DATA/"
        + "meshtest/XrayCentering_01/mesh-meshtest_1_1_master.h5"
    )
    h5DataFilePath1Reference = pathlib.Path(
        "/data/id30a3/inhouse/opid30a3/20160204/RAW_DATA/"
        + "meshtest/XrayCentering_01/mesh-meshtest_1_1_data_000001.h5"
    )
    assert h5MasterFilePath1 == h5MasterFilePath1Reference
    assert h5DataFilePath1 == h5DataFilePath1Reference


def testGetH5FilePath_fastMesh():
    filePath2 = pathlib.Path(
        "/data/id30a3/inhouse/opid30a3/20171017/RAW_DATA/"
        + "mesh2/MeshScan_02/mesh-opid30a3_2_0021.cbf"
    )
    (
        h5MasterFilePath2,
        h5DataFilePath2,
        h5FileNumber2,
    ) = ImageQualityIndicators.getH5FilePath(filePath2, batchSize=20, isFastMesh=True)
    h5MasterFilePath2Reference = pathlib.Path(
        "/data/id30a3/inhouse/opid30a3/20171017/RAW_DATA/"
        + "mesh2/MeshScan_02/mesh-opid30a3_2_1_master.h5"
    )
    assert h5MasterFilePath2 == h5MasterFilePath2Reference
    h5DataFilePath2Reference = pathlib.Path(
        "/data/id30a3/inhouse/opid30a3/20171017/RAW_DATA/"
        + "mesh2/MeshScan_02/mesh-opid30a3_2_1_data_000001.h5"
    )
    assert h5DataFilePath2 == h5DataFilePath2Reference
    #
    # fast mesh 2
    #
    filePath2 = pathlib.Path(
        "/data/id30a3/inhouse/opid30a3/20171017/RAW_DATA/mesh2"
        + "/MeshScan_02/mesh-opid30a3_2_0321.cbf"
    )
    (
        h5MasterFilePath2,
        h5DataFilePath2,
        h5FileNumber2,
    ) = ImageQualityIndicators.getH5FilePath(filePath2, batchSize=20, isFastMesh=True)
    h5MasterFilePath2Reference = pathlib.Path(
        "/data/id30a3/inhouse/opid30a3/20171017/RAW_DATA/mesh2/"
        + "MeshScan_02/mesh-opid30a3_2_1_master.h5"
    )
    assert h5MasterFilePath2 == h5MasterFilePath2Reference
    h5DataFilePath2Reference = pathlib.Path(
        "/data/id30a3/inhouse/opid30a3/20171017/RAW_DATA/mesh2/"
        + "MeshScan_02/mesh-opid30a3_2_1_data_000004.h5"
    )
    assert h5DataFilePath2 == h5DataFilePath2Reference
