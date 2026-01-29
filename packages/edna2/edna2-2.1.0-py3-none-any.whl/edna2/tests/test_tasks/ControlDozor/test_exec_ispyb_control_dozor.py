import os
import pytest

import edna2.config

from edna2.utils import UtilsTest

from edna2.tasks.ControlDozor import ControlDozor


@pytest.fixture
def data_path():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    return data_path


# TODO : These images don't exist anylonger, new images are needed
@pytest.mark.skipif(
    not edna2.config.get_site().lower().startswith("esrf"),
    reason="Dozor test_getLibrary disabled when using non-ESRF config",
)
@pytest.mark.skipif(
    not os.path.exists(
        "/data/id30a2/inhouse/opid30a2/20200907/RAW_DATA/opid30a2_1_0001.cbf"
    ),
    reason="Test images don't exist",
)
def test_execute_ControlDozor_ispyb(data_path):
    current_site = edna2.config.get_site()
    reference_data_path = data_path / "ControlDozor_ispyb.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    controlDozor = ControlDozor(inData=in_data)
    controlDozor.execute()
    assert controlDozor.isSuccess()
    edna2.config.set_site(current_site)
    out_data = controlDozor.out_data
    assert len(out_data["imageQualityIndicators"]) == 100


# TODO : These images don't exist anylonger, new images are needed
@pytest.mark.skipif(
    not edna2.config.get_site().lower().startswith("esrf"),
    reason="Dozor test_getLibrary disabled when using non-ESRF config",
)
@pytest.mark.skipif(
    not os.path.exists(
        "/data/id30a2/inhouse/opid30a2/20200907/RAW_DATA/opid30a2_1_0001.cbf"
    ),
    reason="Test images don't exist",
)
def test_execute_ControlDozor_ispyb_id30a3(data_path):
    current_site = edna2.config.get_site()
    reference_data_path = data_path / "ControlDozor_ispyb_id30a3.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    controlDozor = ControlDozor(inData=in_data)
    controlDozor.execute()
    assert controlDozor.isSuccess()
    edna2.config.set_site(current_site)
    out_data = controlDozor.out_data
    assert len(out_data["imageQualityIndicators"]) == 4


# TODO : These images don't exist anylonger, new images are needed
@pytest.mark.skipif(
    not edna2.config.get_site().lower().startswith("esrf"),
    reason="Dozor test_getLibrary disabled when using non-ESRF config",
)
@pytest.mark.skipif(
    not os.path.exists(
        "/data/visitor/mx415/id30a3/20171127/RAW_DATA/mx415/"
        + "1-2-2/MXPressF_01/mesh-mx415_1_1_master.h5"
    ),
    reason="Test images don't exist",
)
def test_execute_ControlDozor_ispyb_h5(data_path):
    current_site = edna2.config.get_site()
    reference_data_path = data_path / "ControlDozor_ispyb_hdf5.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    controlDozor = ControlDozor(inData=in_data)
    controlDozor.execute()
    edna2.config.set_site(current_site)
    assert controlDozor.isSuccess()
    out_data = controlDozor.out_data
    assert len(out_data["imageQualityIndicators"]) == 51
