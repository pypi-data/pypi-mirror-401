from edna2.utils import UtilsPath


def test_create_pyarch_file_path():
    assert "None" == str(UtilsPath.createPyarchFilePath("/"))
    assert "None" == str(UtilsPath.createPyarchFilePath("/data"))
    assert "None" == str(UtilsPath.createPyarchFilePath("/data/visitor"))
    assert "None" == str(UtilsPath.createPyarchFilePath("/data/visitor/mx415/id14eh2"))
    assert "/data/pyarch/2010/id14eh2/mx415/20100212" == str(
        UtilsPath.createPyarchFilePath(
            "/data/visitor/mx415/id14eh2/20100212"
        ).as_posix()
    )
    assert "/data/pyarch/2010/id14eh2/mx415/20100212/1" == str(
        UtilsPath.createPyarchFilePath(
            "/data/visitor/mx415/id14eh2/20100212/1"
        ).as_posix()
    )
    assert "/data/pyarch/2010/id14eh2/mx415/20100212/1/2" == str(
        UtilsPath.createPyarchFilePath(
            "/data/visitor/mx415/id14eh2/20100212/1/2"
        ).as_posix()
    )
    # Test with inhouse account...
    assert "None" == str(UtilsPath.createPyarchFilePath("/"))
    assert "None" == str(UtilsPath.createPyarchFilePath("/data"))
    assert "None" == str(UtilsPath.createPyarchFilePath("/data/id23eh2"))
    assert "None" == str(UtilsPath.createPyarchFilePath("/data/id23eh2/inhouse"))
    assert "None" == str(
        UtilsPath.createPyarchFilePath("/data/id23eh2/inhouse/opid232")
    )
    assert "/data/pyarch/2010/id23eh2/opid232/20100525" == str(
        UtilsPath.createPyarchFilePath(
            "/data/id23eh2/inhouse/opid232/20100525"
        ).as_posix()
    )
    assert "/data/pyarch/2010/id23eh2/opid232/20100525/1" == str(
        UtilsPath.createPyarchFilePath(
            "/data/id23eh2/inhouse/opid232/20100525/1"
        ).as_posix()
    )
    assert "/data/pyarch/2010/id23eh2/opid232/20100525/1/2" == str(
        UtilsPath.createPyarchFilePath(
            "/data/id23eh2/inhouse/opid232/20100525/1/2"
        ).as_posix()
    )
    assert (
        "/data/pyarch/2014/id30a1/opid30a1/20140717/RAW_DATA/opid30a1_1_dnafiles"
        == str(
            UtilsPath.createPyarchFilePath(
                "/data/id30a1/inhouse/opid30a1/20140717/RAW_DATA/opid30a1_1_dnafiles"
            ).as_posix()
        )
    )
    # Visitor
    assert "None" == str(UtilsPath.createPyarchFilePath("/data/visitor/mx415/id30a3"))
    assert "/data/pyarch/2010/id30a3/mx415/20100212" == str(
        UtilsPath.createPyarchFilePath("/data/visitor/mx415/id30a3/20100212").as_posix()
    )
    assert "/data/pyarch/2010/id30a3/mx415/20100212/1" == str(
        UtilsPath.createPyarchFilePath(
            "/data/visitor/mx415/id30a3/20100212/1"
        ).as_posix()
    )
    assert "/data/pyarch/2010/id30a3/mx415/20100212/1/2" == str(
        UtilsPath.createPyarchFilePath(
            "/data/visitor/mx415/id30a3/20100212/1/2"
        ).as_posix()
    )
    assert "/data/pyarch/2010/id30a3/opid232/20100525" == str(
        UtilsPath.createPyarchFilePath(
            "/data/id30a3/inhouse/opid232/20100525"
        ).as_posix()
    )
    assert "/data/pyarch/2010/id30a3/opid232/20100525/1" == str(
        UtilsPath.createPyarchFilePath(
            "/data/id30a3/inhouse/opid232/20100525/1"
        ).as_posix()
    )
    assert "/data/pyarch/2010/id30a3/opid232/20100525/1/2" == str(
        UtilsPath.createPyarchFilePath(
            "/data/id30a3/inhouse/opid232/20100525/1/2"
        ).as_posix()
    )
    assert (
        "/data/pyarch/2014/id30a3/opid30a1/20140717/RAW_DATA/opid30a1_1_dnafiles"
        == str(
            UtilsPath.createPyarchFilePath(
                "/data/id30a3/inhouse/opid30a1/20140717/RAW_DATA/opid30a1_1_dnafiles"
            ).as_posix()
        )
    )
    #     # Test with different prefix...:
    assert "/data/pyarch/2010/id23eh2/opid232/20100525" == str(
        UtilsPath.createPyarchFilePath(
            "/mnt/multipath-shares/data/id23eh2/inhouse/opid232/20100525"
        ).as_posix()
    )


def test_strip_data_directory_prefix():
    data_directory = "/gpfs/easy/data/id30a2/inhouse/opid30a2"
    new_data_directory = UtilsPath.stripDataDirectoryPrefix(data_directory).as_posix()
    assert str(new_data_directory) == "/data/id30a2/inhouse/opid30a2"
