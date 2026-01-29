import pytest
import pathlib

from edna2.utils import UtilsDnaTables
from edna2.utils import UtilsLogging

logger = UtilsLogging.getLogger()


@pytest.fixture
def data_path():
    data_path = pathlib.Path(__file__).parent / "data"
    return data_path


def test_getDict(data_path):
    dict_dna_tables = UtilsDnaTables.getDict(
        data_path / "indexingTwoImagesDnaTables.xml"
    )
    # logger.info(pprint.pformat(dictDnaTables))
    assert dict_dna_tables is not None


def test_getTables(data_path):
    dict_dna_tables = UtilsDnaTables.getDict(
        data_path / "indexingTwoImagesDnaTables.xml"
    )
    list_tables = UtilsDnaTables.getTables(dict_dna_tables, "autoindex_solutions")
    # logger.info(pprint.pformat(listTables))
    assert len(list(list_tables)) >= 1


def test_getListParam(data_path):
    dict_dna_tables = UtilsDnaTables.getDict(
        data_path / "indexingTwoImagesDnaTables.xml"
    )
    list_tables = UtilsDnaTables.getTables(dict_dna_tables, "autoindex_solutions")
    list_parameter = UtilsDnaTables.getListParam(list_tables[0])
    # logger.info(pprint.pformat(listParameter))
    assert len(list_parameter) >= 1


def test_getItemValue(data_path):
    dict_dna_tables = UtilsDnaTables.getDict(
        data_path / "indexingTwoImagesDnaTables.xml"
    )
    list_tables = UtilsDnaTables.getTables(dict_dna_tables, "autoindex_solutions")
    list_parameter = UtilsDnaTables.getListParam(list_tables[0])
    dict_param = list_parameter[0]
    # logger.info(pprint.pformat(dictParam))
    assert UtilsDnaTables.getItemValue(dict_param, "penalty") == 999
    assert UtilsDnaTables.getItemValue(dict_param, "lattice") == "cI"
    assert UtilsDnaTables.getItemValue(dict_param, "a") == 121.869148


def test_getListValue(data_path):
    # Mosaicity
    dict_dna_tables = UtilsDnaTables.getDict(
        data_path / "indexingTwoImagesDnaTables.xml"
    )
    list_tables = UtilsDnaTables.getTables(dict_dna_tables, "mosaicity_estimation")
    list_parameter = UtilsDnaTables.getListParam(list_tables[0])
    # logger.info(pprint.pformat(listParameter))
    assert UtilsDnaTables.getListValue(list_parameter, "mosaicity", "value") == 0.1
    # Refinement
    list_tables_refinement = UtilsDnaTables.getTables(dict_dna_tables, "refinement")
    table_refinement = list_tables_refinement[0]
    list_param_refinement = UtilsDnaTables.getListParam(table_refinement)
    # logger.info(pprint.pformat(listParamRefinement))
    assert (
        UtilsDnaTables.getListValue(list_param_refinement, "parameters", "used") == 204
    )
    assert (
        UtilsDnaTables.getListValue(
            list_param_refinement, "results", "detector_distance"
        )
        == 305.222015
    )
    assert (
        UtilsDnaTables.getListValue(list_param_refinement, "deviations", "positional")
        == 1.351692
    )
