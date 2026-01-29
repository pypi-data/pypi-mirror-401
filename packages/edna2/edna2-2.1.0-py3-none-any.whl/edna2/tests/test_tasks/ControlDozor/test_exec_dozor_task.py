import os
import edna2
import pytest

from edna2.tasks.ControlDozor import ExecDozor

from edna2.utils import UtilsTest


@pytest.fixture
def data_path():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    return data_path


@pytest.mark.skipif(
    not edna2.config.get_site().lower().startswith("esrf"),
    reason="Dozor execution test disabled when using non-ESRF config",
)
def test_execute_Dozor(data_path):
    reference_data_path = data_path / "inDataDozor.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    # 'Manually' load the 10 test images
    for image_no in range(1, 11):
        file_name = "x_1_{0:04d}.cbf".format(image_no)
        UtilsTest.loadTestImage(file_name)
    dozor = ExecDozor(inData=in_data)
    dozor.execute()
    assert dozor.isSuccess()
    out_data = dozor.outData
    assert len(out_data["imageDozor"]) == 10


@pytest.mark.skipif(
    not edna2.config.get_site().lower().startswith("esrf"),
    reason="Dozor execution test disabled when using non-ESRF config",
)
def test_execute_Dozor_slurm(data_path):
    reference_data_path = data_path / "inDataDozor.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    in_data["doSubmit"] = True
    # Load the 10 test images
    for image_no in range(1, 11):
        file_name = "x_1_{0:04d}.cbf".format(image_no)
        UtilsTest.loadTestImage(file_name)
    dozor = ExecDozor(inData=in_data)
    dozor.execute()
    assert dozor.isSuccess()
    out_data = dozor.outData
    assert len(out_data["imageDozor"]) == 10


# TODO : These images don't exist anylonger, new images are needed
@pytest.mark.skipif(
    not edna2.config.get_site().lower().startswith("esrf"),
    reason="Dozor execution test disabled when using non-ESRF config",
)
@pytest.mark.skipif(
    not os.path.exists(
        "/data/visitor/mx415/id30a3/20171127/"
        + "RAW_DATA/mx415/1-2-2/MXPressF_01/"
        + "mesh-mx415_1_1_master.h5"
    ),
    reason="Test images don't exist",
)
def test_execute_ExecDozor_eiger4m(data_path):
    # edna2.config.set_site('esrf_ispyb_valid')
    reference_data_path = data_path / "ExecDozor_eiger4m.json"
    in_data = UtilsTest.loadAndSubstitueTestData(reference_data_path)
    dozor = ExecDozor(inData=in_data)
    dozor.execute()
    assert dozor.isSuccess()
    out_data = dozor.outData
    assert len(out_data["imageDozor"]) == 51
