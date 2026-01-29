import pytest
import pathlib

from edna2.utils import UtilsImage


@pytest.fixture
def image_file_name():
    return "ref-testscale_1_0001.img"


@pytest.fixture
def image_file_name2():
    return "ref-testscale_1_12345.img"


@pytest.fixture
def image_file_name_h5():
    return "mesh-local-user_0_1_000001.h5"


def test_getPrefix(image_file_name):
    prefix = UtilsImage.getPrefix(image_file_name)
    assert prefix == "ref-testscale_1"


def test_getPrefixH5(image_file_name_h5):
    prefix = UtilsImage.getPrefix(image_file_name_h5)
    assert prefix == "mesh-local-user_0_1"


def test_getImageNumber(image_file_name):
    image_number = UtilsImage.getImageNumber(image_file_name)
    assert image_number == 1


def test_getTemplateHash(image_file_name):
    template = UtilsImage.getTemplate(image_file_name)
    template_reference = "ref-testscale_1_####.img"
    assert template_reference == template


def test_getTemplateHash2(image_file_name2):
    template = UtilsImage.getTemplate(image_file_name2)
    template_reference = "ref-testscale_1_#####.img"
    assert template_reference == template


def test_getTemplateQuestionMark(image_file_name):
    template = UtilsImage.getTemplate(image_file_name, symbol="?")
    template_reference = "ref-testscale_1_????.img"
    assert template_reference == template


def test_getH5FilePath_ref():
    ref_h5_master1 = "ref-UPF2-UPF2__4_1_1_master.h5"
    ref_h5_data1 = "ref-UPF2-UPF2__4_1_1_data_000001.h5"
    file1 = "ref-UPF2-UPF2__4_1_0001.h5"
    h5_master_file_path, h5_data_file_path, _ = UtilsImage.getH5FilePath(
        file1, hasOverlap=True
    )
    assert ref_h5_master1 == str(h5_master_file_path)
    assert ref_h5_data1 == str(h5_data_file_path)

    ref_h5_master2 = "ref-UPF2-UPF2__4_1_2_master.h5"
    ref_h5_data2 = "ref-UPF2-UPF2__4_1_2_data_000001.h5"
    file2 = "ref-UPF2-UPF2__4_1_0002.h5"
    h5_master_file_path, h5_data_file_path, _ = UtilsImage.getH5FilePath(
        file2, hasOverlap=True
    )
    assert ref_h5_master2 == str(h5_master_file_path)
    assert ref_h5_data2 == str(h5_data_file_path)


def test_splitPrefixRunNumber():
    path = pathlib.Path(
        "/data/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/PsPL7C-252_1_0001.cbf"
    )
    pre_prefix, run_number = UtilsImage.splitPrefixRunNumber(path)
    assert pre_prefix == "PsPL7C-252"
    assert run_number == 1

    path = pathlib.Path(
        "/data/scisoft/pxsoft/data/EDNA2_INDEXING/id23eh1/EX1/Ps_PL_7C-2_52_1_0001.cbf"
    )
    pre_prefix, run_number = UtilsImage.splitPrefixRunNumber(path)
    assert pre_prefix == "Ps_PL_7C-2_52"
    assert run_number == 1


def test_template_to_format():
    # CBF, four hashes
    template = "ref-testscale_1_####.cbf"
    format = UtilsImage.template_to_format(template)
    assert format == "ref-testscale_1_%04d.cbf"
    # H5, four hashes
    template = "ref-testscale_1_####.h5"
    format = UtilsImage.template_to_format(template)
    assert format == "ref-testscale_1_%04d.h5"
    # H5, six hashes
    template = "ref-testscale_1_######.h5"
    format = UtilsImage.template_to_format(template)
    assert format == "ref-testscale_1_%06d.h5"


def test_template_to_image_name():
    # CBF, four hashes
    template = "ref-testscale_1_####.cbf"
    image_name = UtilsImage.template_to_image_name(template, image_number=123)
    assert image_name == "ref-testscale_1_0123.cbf"
    # H5, four hashes
    template = "ref-testscale_1_####.h5"
    image_name = UtilsImage.template_to_image_name(template, image_number=123)
    assert image_name == "ref-testscale_1_0123.h5"
    # H5, six hashes
    template = "ref-testscale_1_######.h5"
    image_name = UtilsImage.template_to_image_name(template, image_number=123)
    assert image_name == "ref-testscale_1_000123.h5"
    # H5, four hashes, six digits
    template = "ref-testscale_1_####.h5"
    image_name = UtilsImage.template_to_image_name(
        template, image_number=123, no_digits=6
    )
    assert image_name == "ref-testscale_1_000123.h5"
