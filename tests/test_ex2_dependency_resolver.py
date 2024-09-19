import pytest
import json
import os
from io import StringIO
import sys
from src.ex2_dependency_resolver import load_deps, resolve_deps, pprint

# ------------ Helper functions ------------

# Helper function to get the path of a data file
def get_data_file_path(filename):
    return os.path.join(os.path.dirname(__file__), '..', 'data', filename)

# Helper function to capture stdout
# got help from here: https://docs.pytest.org/en/stable/how-to/capture-stdout-stderr.html
# and here: https://docs.python.org/3/library/sys.html#sys.__stdout__
def capture_stdout(func, *args, **kwargs):
    captured_output = StringIO()            # Create a StringIO object to capture the output of the print statements
    sys.stdout = captured_output            # Redirect sys.stdout to the StringIO object so that any print statements inside the 'func' will write to 'captured_output' instead of the console
    func(*args, **kwargs)                   # Execute the function 'func' with its arguments and keyword arguments
    sys.stdout = sys.__stdout__             # Restore sys.stdout to its original state (the default stdout)
    return captured_output.getvalue()       # Return the captured output as a string

# ------------ Tests for the structure of the generated graph ------------

def test_resolve_deps_simple1():
    file_path = get_data_file_path('simple_deps1.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    output = capture_stdout(resolve_deps, data)
    expected_output = "-pkg1\n  -pkg2\n    -pkg3\n  -pkg3\n-pkg2\n  -pkg3\n-pkg3\n"
    assert output == expected_output

def test_resolve_deps_simple2():
    file_path = get_data_file_path('simple_deps2.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    output = capture_stdout(resolve_deps, data)
    expected_output = "-pkg1\n  -pkg3\n  -pkg2\n-pkg2\n  -pkg3\n-pkg3\n"
    assert output == expected_output

def test_resolve_deps_complex():
    file_path = get_data_file_path('complex_deps.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    output = capture_stdout(resolve_deps, data)
    expected_output = "-pkg1\n  -pkg2\n    -pkg3\n      -pkg5\n    -pkg5\n  -pkg3\n    -pkg5\n  -pkg4\n    -pkg5\n    -pkg6\n-pkg2\n  -pkg3\n    -pkg5\n  -pkg5\n-pkg3\n  -pkg5\n-pkg4\n  -pkg5\n  -pkg6\n-pkg5\n-pkg6\n"
    assert output == expected_output

def test_resolve_deps_circular():
    file_path = get_data_file_path('circular_deps.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    output = capture_stdout(resolve_deps, data)
    expected_output = "-pkg1\n  -pkg2\n    -pkg3\n-pkg2\n  -pkg3\n-pkg3\n"
    assert output == expected_output

def test_resolve_deps_empty():
    file_path = get_data_file_path('empty_deps.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    output = capture_stdout(resolve_deps, data)
    assert output == ""

def test_resolve_deps_single_package():
    file_path = get_data_file_path('single_package_deps.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    output = capture_stdout(resolve_deps, data)
    expected_output = "-pkg1\n"
    assert output == expected_output

# ------------ Errors related to json and the data itself ------------

def test_resolve_deps_missing_dependency():
    file_path = get_data_file_path('missing_dep_deps.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    with pytest.raises(KeyError):
        resolve_deps(data)

def test_resolve_deps_invalid_json():
    invalid_json = '{"pkg1": ["pkg2"], "pkg2": [}'
    with pytest.raises(json.JSONDecodeError):
        resolve_deps(json.loads(invalid_json))

def test_resolve_deps_non_list_dependency():
    invalid_data = {"pkg1": "pkg2", "pkg2": []}
    with pytest.raises(TypeError):
        resolve_deps(invalid_data)

def test_resolve_deps_self_dependency():
    self_dep_data = {"pkg1": ["pkg1"], "pkg2": []}
    output = capture_stdout(resolve_deps, self_dep_data)
    expected_output = "-pkg1\n-pkg2\n"
    assert output == expected_output

def test_resolve_deps_non_string_key():
    invalid_data = {1: ["pkg1"], "pkg1": []}
    with pytest.raises(TypeError):
        resolve_deps(invalid_data)
