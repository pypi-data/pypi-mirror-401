from edna2.utils import UtilsSymmetry


def test_getMinimumSymmetrySpaceGroupFromBravaisLattice():
    """
    Testing retrieving the lowest symmetry space group from all Bravais Lattices
    """
    listBravaisLattice = [
        "aP",
        "mP",
        "mC",
        "mI",
        "oP",
        "oA",
        "oB",
        "oC",
        "oS",
        "oF",
        "oI",
        "tP",
        "tC",
        "tI",
        "tF",
        "hP",
        "hR",
        "cP",
        "cF",
        "cI",
    ]
    listSpaceGroup = [
        "P1",
        "P2",
        "C2",
        "C2",
        "P222",
        "C222",
        "C222",
        "C222",
        "C222",
        "F222",
        "I222",
        "P4",
        "P4",
        "I4",
        "I4",
        "P3",
        "H3",
        "P23",
        "F23",
        "I23",
    ]
    for index in range(len(listBravaisLattice)):
        assert listSpaceGroup[
            index
        ] == UtilsSymmetry.getMinimumSymmetrySpaceGroupFromBravaisLattice(
            listBravaisLattice[index]
        )


def test_getITNumberFromSpaceGroupName():
    assert 1 == UtilsSymmetry.getITNumberFromSpaceGroupName("P1")
    assert 3 == UtilsSymmetry.getITNumberFromSpaceGroupName("P2")
    assert 5 == UtilsSymmetry.getITNumberFromSpaceGroupName("C2")
    assert 16 == UtilsSymmetry.getITNumberFromSpaceGroupName("P222")
    assert 21 == UtilsSymmetry.getITNumberFromSpaceGroupName("C222")
    assert 22 == UtilsSymmetry.getITNumberFromSpaceGroupName("F222")
    assert 75 == UtilsSymmetry.getITNumberFromSpaceGroupName("P4")
    assert 79 == UtilsSymmetry.getITNumberFromSpaceGroupName("I4")
    assert 143 == UtilsSymmetry.getITNumberFromSpaceGroupName("P3")
    assert 146 == UtilsSymmetry.getITNumberFromSpaceGroupName("H3")
    assert 195 == UtilsSymmetry.getITNumberFromSpaceGroupName("P23")
    assert 196 == UtilsSymmetry.getITNumberFromSpaceGroupName("F23")


def test_getSpaceGroupNameFromITNumber():
    assert "P1" == UtilsSymmetry.getSpaceGroupNameFromITNumber(1)
    assert "P2" == UtilsSymmetry.getSpaceGroupNameFromITNumber(3)
    assert "C2" == UtilsSymmetry.getSpaceGroupNameFromITNumber(5)
    assert "P222" == UtilsSymmetry.getSpaceGroupNameFromITNumber(16)
    assert "C222" == UtilsSymmetry.getSpaceGroupNameFromITNumber(21)
    assert "F222" == UtilsSymmetry.getSpaceGroupNameFromITNumber(22)
    assert "P4" == UtilsSymmetry.getSpaceGroupNameFromITNumber(75)
    assert "I4" == UtilsSymmetry.getSpaceGroupNameFromITNumber(79)
    assert "P3" == UtilsSymmetry.getSpaceGroupNameFromITNumber(143)
    assert "H3" == UtilsSymmetry.getSpaceGroupNameFromITNumber(146)
    assert "P23" == UtilsSymmetry.getSpaceGroupNameFromITNumber(195)
    assert "F23" == UtilsSymmetry.getSpaceGroupNameFromITNumber(196)


def test_get_short_space_group_name():
    assert "P1" == UtilsSymmetry.get_short_space_group_name("P 1")
    assert "P1" == UtilsSymmetry.get_short_space_group_name("P1")
    assert "P2" == UtilsSymmetry.get_short_space_group_name("P 1 2 1")
    assert "P2" == UtilsSymmetry.get_short_space_group_name("P2")
    assert "C2" == UtilsSymmetry.get_short_space_group_name("C 1 2 1")
    assert "P222" == UtilsSymmetry.get_short_space_group_name("P 2 2 2")
    assert "C222" == UtilsSymmetry.get_short_space_group_name("C 2 2 2")
    assert "F222" == UtilsSymmetry.get_short_space_group_name("F 2 2 2")
    assert "P4" == UtilsSymmetry.get_short_space_group_name("P 4")
    assert "I4" == UtilsSymmetry.get_short_space_group_name("I 4")
    assert "P3" == UtilsSymmetry.get_short_space_group_name("P 3")
    assert "H3" == UtilsSymmetry.get_short_space_group_name("H 3")
    assert "P23" == UtilsSymmetry.get_short_space_group_name("P 2 3")
    assert "F23" == UtilsSymmetry.get_short_space_group_name("F 2 3")


def test_get_short_space_group_name_with_space_problem():
    assert "P21" == UtilsSymmetry.get_short_space_group_name("P1 21 1")
    assert "P21" == UtilsSymmetry.get_short_space_group_name("P1211")
