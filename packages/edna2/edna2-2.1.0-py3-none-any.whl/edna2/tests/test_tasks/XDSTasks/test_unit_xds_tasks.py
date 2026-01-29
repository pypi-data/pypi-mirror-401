import pytest

from edna2 import config

from edna2.utils import UtilsTest

from edna2.tasks.XDSTasks import XDSTask
from edna2.tasks.XDSTasks import XDSIndexing


@pytest.fixture
def data_path():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    return data_path


@pytest.mark.skipif(
    True,
    reason="This method is not used any longer and might be removed",
)
def test_createSPOT_XDS(data_path):
    spot_file = data_path / "00001.spot"
    spot_xds_reference_file = data_path / "SPOT.XDS"
    with open(spot_xds_reference_file) as f:
        spot_xds_reference = f.read()
    spot_xds = XDSTask.createSPOT_XDS([spot_file], oscRange=1)
    assert spot_xds_reference.split("\n")[0] == spot_xds.split("\n")[0]
    assert spot_xds_reference == spot_xds


def test_readIdxrefLp(data_path):
    idx_ref_lp_path = data_path / "IDXREF_TRYP.LP"
    result_xds_indexing = XDSIndexing.readIdxrefLp(idx_ref_lp_path)
    assert result_xds_indexing["spaceGroupNumber"] == 75


@pytest.mark.skipif(
    True,
    reason="Disabled during XDS tasks refactoring",
)
def test_parseXparm(data_path):
    xparm_path = data_path / "XPARM.XDS"
    xparm_dict = XDSIndexing.parseXparm(xparm_path)
    assert xparm_dict["symmetry"] == 1


@pytest.mark.skipif(
    True,
    reason="Disabled during XDS tasks refactoring",
)
def test_getXDSDetector(data_path):
    reference_data_path = data_path / "inDataXDSIndexing.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    first_sub_wedge = in_data["subWedge"][0]
    dict_detector = first_sub_wedge["experimentalCondition"]["detector"]
    dict_xds_detector = XDSTask.getXDSDetector(dict_detector)
    assert dict_xds_detector["name"] == "PILATUS"


@pytest.mark.skipif(
    True,
    reason="Disabled during XDS tasks refactoring",
)
def test_generateXDS_INP(data_path):
    reference_data_path = data_path / "inDataXDSIndexing.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    list_xds_inp = XDSTask.generateXDS_INP(in_data)
    assert list_xds_inp[0] == "OVERLOAD=10048500"


@pytest.mark.skipif(
    True,
    reason="Disabled during XDS tasks refactoring",
)
@pytest.mark.skipif(
    not config.get_site().lower().startswith("esrf"),
    reason="XDS link generation test disabled when using non-ESRF config",
)
def test_generateImageLinks_1(tmpdir, data_path):
    reference_data_path = data_path / "inDataXDSIntegration.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    dict_image_links = XDSTask.generateImageLinks(in_data, working_directory=tmpdir)
    link_source_1 = dict_image_links["imageLink"][0][0][0]
    link_target_1 = dict_image_links["imageLink"][0][0][1]
    path_target_1 = tmpdir / link_target_1
    assert path_target_1.readlink() == link_source_1


@pytest.mark.skipif(
    True,
    reason="Disabled during XDS tasks refactoring",
)
@pytest.mark.skipif(
    not config.get_site().lower().startswith("esrf"),
    reason="XDS link generation test disabled when using non-ESRF config",
)
def test_generateImageLinks_2(tmpdir, data_path):
    reference_data_path = data_path / "inDataXDSIntegration_one_subWedge.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    dict_image_links = XDSTask.generateImageLinks(in_data, working_directory=tmpdir)
    link_source_1 = dict_image_links["imageLink"][0][0][0]
    link_target_1 = dict_image_links["imageLink"][0][0][1]
    path_target_1 = tmpdir / link_target_1
    assert path_target_1.readlink() == link_source_1


@pytest.mark.skipif(
    True,
    reason="Disabled during XDS tasks refactoring",
)
def test_generateImageLinks_3(tmpdir, data_path):
    reference_data_path = data_path / "inDataXDSGenerateBackground_eiger16m.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    dict_image_links = XDSTask.generateImageLinks(in_data, working_directory=tmpdir)
    link_source_1 = dict_image_links["imageLink"][0][0][0]
    link_target_1 = dict_image_links["imageLink"][0][0][1]
    path_target_1 = tmpdir / link_target_1
    assert path_target_1.readlink() == link_source_1


@pytest.mark.skipif(
    True,
    reason="Disabled during XDS tasks refactoring",
)
def test_generateImageLinks_4(tmpdir, data_path):
    reference_data_path = data_path / "id30a1_1_fast_char.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    dict_image_links = XDSTask.generateImageLinks(in_data, working_directory=tmpdir)
    link_source_1 = dict_image_links["imageLink"][0][0][0]
    link_target_1 = dict_image_links["imageLink"][0][0][1]
    path_target_1 = tmpdir / link_target_1
    assert path_target_1.readlink() == link_source_1
