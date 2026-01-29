import copy
import json
import pytest
import pathlib

from edna2.utils import UtilsSubWedge
from edna2.utils import UtilsLogging

logger = UtilsLogging.getLogger()


@pytest.fixture
def exp_cond_ref():
    data_path = pathlib.Path(__file__).parent / "data"
    test_file_path = data_path / "experimentalCondition.json"
    with open(test_file_path) as f:
        exp_cond_ref = json.loads(f.read())
    return exp_cond_ref


@pytest.fixture
def list_sub_wedge():
    data_path = pathlib.Path(__file__).parent / "data"
    test_file_path = data_path / "listSubWedge.json"
    with open(test_file_path) as f:
        list_sub_wedge = json.loads(f.read())
    return list_sub_wedge


@pytest.fixture
def list_of_10_sub_wedges():
    data_path = pathlib.Path(__file__).parent / "data"
    test_file_path = data_path / "listOf10SubWedges.json"
    with open(test_file_path) as f:
        list_sub_wedge = json.loads(f.read())
    return list_sub_wedge


def test_compare_two_values():
    assert UtilsSubWedge.compare_two_values(1, 1)
    assert not UtilsSubWedge.compare_two_values(1, 2)
    assert UtilsSubWedge.compare_two_values(1.0, 1.0)
    assert not UtilsSubWedge.compare_two_values(1.0, 1.01)
    assert UtilsSubWedge.compare_two_values(1.0, 1.01, 0.1)
    assert UtilsSubWedge.compare_two_values("EDNA", "EDNA")
    assert not UtilsSubWedge.compare_two_values("EDNA", "DNA")
    # Comparison of two different types should raise an exception
    try:
        _ = UtilsSubWedge.compare_two_values("EDNA", 1)
        raise RuntimeError("Problem - exception not raised")
    except Exception:
        assert True
    # Comparison of anything but double, int or string should raise an exception
    try:
        _ = UtilsSubWedge.compare_two_values([1], [1])
        raise RuntimeError("Problem - exception not raised")
    except Exception:
        assert True


def test_is_same_experimental_condition(exp_cond_ref):
    exp_cond_ref2 = dict(exp_cond_ref)
    assert UtilsSubWedge.isSameExperimentalCondition(exp_cond_ref, exp_cond_ref2)


def test_is_same_experimental_condition_2(exp_cond_ref):
    exp_cond_different_exp_time = copy.deepcopy(exp_cond_ref)
    exp_cond_different_exp_time["beam"]["exposureTime"] += 1
    assert not UtilsSubWedge.isSameExperimentalCondition(
        exp_cond_ref, exp_cond_different_exp_time
    )


def test_is_same_experimental_condition_3(exp_cond_ref):
    exp_cond_different_wavelength = copy.deepcopy(exp_cond_ref)
    exp_cond_different_wavelength["beam"]["wavelength"] += 1
    assert not UtilsSubWedge.isSameExperimentalCondition(
        exp_cond_ref, exp_cond_different_wavelength
    )


def test_is_same_experimental_condition_4(exp_cond_ref):
    exp_cond_different_beam_position_x = copy.deepcopy(exp_cond_ref)
    exp_cond_different_beam_position_x["detector"]["beamPositionX"] += 1
    assert not UtilsSubWedge.isSameExperimentalCondition(
        exp_cond_ref, exp_cond_different_beam_position_x
    )


def test_is_same_experimental_condition_5(exp_cond_ref):
    exp_cond_different_beam_position_y = copy.deepcopy(exp_cond_ref)
    exp_cond_different_beam_position_y["detector"]["beamPositionY"] += 1
    assert not UtilsSubWedge.isSameExperimentalCondition(
        exp_cond_ref, exp_cond_different_beam_position_y
    )


def test_is_same_experimental_condition_6(exp_cond_ref):
    exp_cond_different_distance = copy.deepcopy(exp_cond_ref)
    exp_cond_different_distance["detector"]["distance"] += 1
    assert not UtilsSubWedge.isSameExperimentalCondition(
        exp_cond_ref, exp_cond_different_distance
    )


def test_is_same_experimental_condition_7(exp_cond_ref):
    exp_cond_different_name = copy.deepcopy(exp_cond_ref)
    exp_cond_different_name["detector"]["name"] = "EDNA"
    assert not UtilsSubWedge.isSameExperimentalCondition(
        exp_cond_ref, exp_cond_different_name
    )


def test_is_same_experimental_condition_8(exp_cond_ref):
    exp_cond_different_number_pixel_x = copy.deepcopy(exp_cond_ref)
    exp_cond_different_number_pixel_x["detector"]["numberPixelX"] += 1
    assert not UtilsSubWedge.isSameExperimentalCondition(
        exp_cond_ref, exp_cond_different_number_pixel_x
    )


def test_is_same_experimental_condition_9(exp_cond_ref):
    exp_cond_different_number_pixel_y = copy.deepcopy(exp_cond_ref)
    exp_cond_different_number_pixel_y["detector"]["numberPixelY"] += 1
    assert not UtilsSubWedge.isSameExperimentalCondition(
        exp_cond_ref, exp_cond_different_number_pixel_y
    )


def test_is_same_experimental_condition_10(exp_cond_ref):
    exp_cond_different_serial_number = copy.deepcopy(exp_cond_ref)
    exp_cond_different_serial_number["detector"]["serialNumber"] = "EDNA"
    assert not UtilsSubWedge.isSameExperimentalCondition(
        exp_cond_ref, exp_cond_different_serial_number
    )


def test_is_same_experimental_condition_11(exp_cond_ref):
    exp_cond_different_two_theta = copy.deepcopy(exp_cond_ref)
    exp_cond_different_two_theta["detector"]["twoTheta"] += 1
    assert not UtilsSubWedge.isSameExperimentalCondition(
        exp_cond_ref, exp_cond_different_two_theta
    )


def test_is_same_experimental_condition_12(exp_cond_ref):
    exp_cond_different_oscillation_width = copy.deepcopy(exp_cond_ref)
    exp_cond_different_oscillation_width["goniostat"]["oscillationWidth"] += 1
    assert not UtilsSubWedge.isSameExperimentalCondition(
        exp_cond_ref, exp_cond_different_oscillation_width
    )


def test_is_same_experimental_condition_13(exp_cond_ref):
    exp_cond_different_rotation_axis = copy.deepcopy(exp_cond_ref)
    exp_cond_different_rotation_axis["goniostat"]["rotationAxis"] = "EDNA"
    assert not UtilsSubWedge.isSameExperimentalCondition(
        exp_cond_ref, exp_cond_different_rotation_axis
    )


def test_sort_identical_objects():
    listObjects = []
    listSorted = UtilsSubWedge.sortIdenticalObjects(
        listObjects, UtilsSubWedge.compare_two_values
    )
    assert listSorted == []
    listObjects = [1]
    listSorted = UtilsSubWedge.sortIdenticalObjects(
        listObjects, UtilsSubWedge.compare_two_values
    )
    assert listSorted == [[1]]
    listObjects = [1, 2]
    listSorted = UtilsSubWedge.sortIdenticalObjects(
        listObjects, UtilsSubWedge.compare_two_values
    )
    assert listSorted == [[1], [2]]
    listObjects = [1, 1]
    listSorted = UtilsSubWedge.sortIdenticalObjects(
        listObjects, UtilsSubWedge.compare_two_values
    )
    assert listSorted == [[1, 1]]
    listObjects = [1, 2, 1, 3, 4, 1, 5, 2, 2, 9, 3, 2]
    listSorted = UtilsSubWedge.sortIdenticalObjects(
        listObjects, UtilsSubWedge.compare_two_values
    )
    assert listSorted == [[1, 1, 1], [2, 2, 2, 2], [3, 3], [4], [5], [9]]


def test_sort_sub_wedges_on_experimental_condition(list_sub_wedge):
    # First check two sub wedges with identical experimental conditions
    list_sub_wedge_sorted = UtilsSubWedge.sortSubWedgesOnExperimentalCondition(
        list_sub_wedge
    )
    # Check that we got a list with one element
    assert len(list_sub_wedge_sorted) == 1
    # Then modify one sub wedge
    list_sub_wedge_modified = copy.deepcopy(list_sub_wedge)
    list_sub_wedge_modified[1]["experimentalCondition"]["detector"]["distance"] += 100.0
    list_sub_wedge_sorted = UtilsSubWedge.sortSubWedgesOnExperimentalCondition(
        list_sub_wedge_modified
    )
    # Check that we got a list with two elements
    assert len(list_sub_wedge_sorted) == 2


def test_merge_two_sub_wedges_adjascent_in_rotation_axis(list_sub_wedge):
    # First check two sub wedges which shouldn't be merged
    list_sub_wedge_copy = copy.deepcopy(list_sub_wedge)
    sub_wedge_1 = list_sub_wedge_copy[0]
    sub_wedge_2 = list_sub_wedge_copy[1]
    sub_wedge_2["experimentalCondition"]["detector"]["distance"] += 100.0
    sub_wedge_should_not_be_merged = (
        UtilsSubWedge.mergeTwoSubWedgesAdjascentInRotationAxis(sub_wedge_1, sub_wedge_2)
    )
    assert sub_wedge_should_not_be_merged is None
    # Then check two adjascent images
    list_sub_wedge_copy = copy.deepcopy(list_sub_wedge)
    sub_wedge_1 = list_sub_wedge_copy[0]
    sub_wedge_2 = list_sub_wedge_copy[1]
    sub_wedge_merged = UtilsSubWedge.mergeTwoSubWedgesAdjascentInRotationAxis(
        sub_wedge_1, sub_wedge_2
    )
    assert len(sub_wedge_merged["image"]) == 2


def test_merge_list_of_sub_wedges_with_adjascent_rotationAxis(list_of_10_sub_wedges):
    # Check a list of ten adjascent images
    sub_wedge_merged = UtilsSubWedge.mergeListOfSubWedgesWithAdjascentRotationAxis(
        list_of_10_sub_wedges
    )
    assert len(sub_wedge_merged[0]["image"]) == 10
