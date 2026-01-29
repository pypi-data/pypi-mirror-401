from edna2.utils import UtilsTest

from edna2.tasks.CCP4Tasks import PointlessTask


def test_unit_PointlessTask():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    path_to_log_file = data_path / "pointless.log"
    out_data = PointlessTask.parsePointlessOutput(path_to_log_file)
    assert "C 2 2 2" == out_data["sgstr"], "Space group name"
    assert 21 == out_data["sgnumber"], "Space group number"
    assert 52.55 == out_data["cell"]["length_a"], "Cell length a"
    assert 148.80 == out_data["cell"]["length_b"], "Cell length b"
    assert 79.68 == out_data["cell"]["length_c"], "Cell length v"
    assert 91.00 == out_data["cell"]["angle_alpha"], "Cell angle alpha"
    assert 92.00 == out_data["cell"]["angle_beta"], "Cell angle beta"
    assert 93.00 == out_data["cell"]["angle_gamma"], "Cell angle gamma"
    pathToLogFile2 = data_path / "pointless2.log"
    out_data = PointlessTask.parsePointlessOutput(pathToLogFile2)
    assert "P 3 2 1" == out_data["sgstr"], "Space group name"
    assert 150 == out_data["sgnumber"], "Space group number"
    assert 110.97 == out_data["cell"]["length_a"], "Cell length a"
    assert 110.97 == out_data["cell"]["length_b"], "Cell length b"
    assert 137.02 == out_data["cell"]["length_c"], "Cell length v"
    assert 90.0 == out_data["cell"]["angle_alpha"], "Cell angle alpha"
    assert 90.0 == out_data["cell"]["angle_beta"], "Cell angle beta"
    assert 119.97 == out_data["cell"]["angle_gamma"], "Cell angle gamma"
