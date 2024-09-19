import pytest
from ex1.src.ex1_duplicate_detector import detect_duplicates

def test_empty_list():
    assert detect_duplicates([]) == []

def test_no_duplicates():
    assert detect_duplicates([1, 2, 3, 4, 5]) == []

def test_with_duplicates():
    assert detect_duplicates(["b", "a", "c", "c", "e", "a", "c", "d", "c", "d"]) == ["a", "c", "d"]

def test_case_sensitivity():
    assert detect_duplicates(["a", "A", "b", "B", "a", "B", "z"]) == ["a", "B"]

def test_unicode_characters():
    assert detect_duplicates(["α", "β", "γ", "α", "δ", "β"]) == ["α", "β"]

def test_all_duplicates():
    assert detect_duplicates([1, 1, 1, 1]) == [1]

def test_mixed_types():
    assert detect_duplicates([1, "a", 2, "b", 1, "a", 3, 2]) == [1, "a", 2]

def test_preserves_first_occurrence_order():
    assert detect_duplicates([3, 1, 2, 1, 3, 2]) == [3, 1, 2]

def test_with_none():
    assert detect_duplicates([None, 1, None, 2, 3, 2]) == [None, 2]

def test_with_booleans():
    assert detect_duplicates([True, False, True, 1, 0, False]) == [True, False]

def test_with_floats():
    assert detect_duplicates([1.0, 2.0, 1.0, 3.0, 2.0]) == [1.0, 2.0]

def test_with_strings():
    assert detect_duplicates("im a string") == ["i", " "]

def test_large_list():
    large_list = list(range(1000000)) + list(range(500000))
    assert detect_duplicates(large_list) == list(range(500000))

# the detect_duplicates function isn't supposed to work with unhashable ("modifiable") types
# like lists. I could have implemented it, but that would be to overengineer something 
# that I think is supposed to be simple...
def test_unhashable_types():
    with pytest.raises(TypeError):
        detect_duplicates([[1], [2], [1], [3], [2]])

def test_non_list_input_none():
    with pytest.raises(TypeError):
        detect_duplicates(None)

def test_non_list_input_int():
    with pytest.raises(TypeError):
        detect_duplicates(42)
