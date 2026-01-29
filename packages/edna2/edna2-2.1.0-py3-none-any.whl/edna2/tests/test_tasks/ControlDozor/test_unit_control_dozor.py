import os
import json

# from controltasks import ControlDozor
from edna2.tasks.ControlDozor import ControlDozor
from edna2.utils import UtilsTest


def testCreateDict():
    data_path = UtilsTest.prepareTestDataPath(__file__)
    reference_data_path = os.path.join(data_path, "ControlDozor.json")
    with open(reference_data_path) as f:
        in_data = json.loads(f.read())
    control_dozor = ControlDozor(inData=in_data)
    dict_image = control_dozor.createImageDict(in_data)
    assert isinstance(dict_image, dict)
    assert ControlDozor.createListOfBatches(range(1, 6), 1) == [[1], [2], [3], [4], [5]]
    assert ControlDozor.createListOfBatches(range(1, 6), 2) == [[1, 2], [3, 4], [5]]
    assert ControlDozor.createListOfBatches(range(1, 6), 3) == [[1, 2, 3], [4, 5]]
    assert ControlDozor.createListOfBatches(range(1, 6), 4) == [[1, 2, 3, 4], [5]]
    assert ControlDozor.createListOfBatches(range(1, 6), 5) == [[1, 2, 3, 4, 5]]
    assert ControlDozor.createListOfBatches(
        list(range(4, 7)) + list(range(1, 3)), 1
    ) == [[1], [2], [4], [5], [6]]
    assert ControlDozor.createListOfBatches(
        list(range(4, 7)) + list(range(1, 3)), 2
    ) == [[1, 2], [4, 5], [6]]
    assert ControlDozor.createListOfBatches(
        list(range(4, 7)) + list(range(1, 3)), 3
    ) == [[1, 2], [4, 5, 6]]
