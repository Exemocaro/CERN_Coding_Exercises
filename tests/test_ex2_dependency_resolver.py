import pytest
import json
import os
from io import StringIO
import sys
from src.ex2_dependency_resolver import load_deps, resolve_deps

# ------------ Helper functions ------------

# Helper function to get the path of a data file
def get_data_file_path(filename):
    return os.path.join(os.path.dirname(__file__), '..', 'data', filename)

# Helper function to load expected output
def load_expected_output(filename):
    file_path = get_data_file_path(filename)
    with open(file_path, 'r') as f:
        return f.read()

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
    file_name = "simple_deps1"
    file_path = get_data_file_path(f'{file_name}.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    output = capture_stdout(resolve_deps, data)
    expected_output = load_expected_output(f'{file_name}.txt')
    assert output == expected_output

def test_resolve_deps_simple2():
    file_name = "simple_deps2"
    file_path = get_data_file_path(f'{file_name}.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    output = capture_stdout(resolve_deps, data)
    expected_output = load_expected_output(f'{file_name}.txt')
    assert output == expected_output

def test_resolve_deps_complex():
    file_name = "complex_deps"
    file_path = get_data_file_path(f'{file_name}.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    output = capture_stdout(resolve_deps, data)
    expected_output = load_expected_output(f'{file_name}.txt')
    assert output == expected_output

def test_resolve_deps_circular():
    file_name = "circular_deps"
    file_path = get_data_file_path(f'{file_name}.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    output = capture_stdout(resolve_deps, data)
    expected_output = load_expected_output(f'{file_name}.txt')
    assert output == expected_output

# yes, this one's output is an empty file...
def test_resolve_deps_empty():
    file_name = "empty_deps"
    file_path = get_data_file_path(f'{file_name}.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    output = capture_stdout(resolve_deps, data)
    expected_output = load_expected_output(f'{file_name}.txt')
    assert output == expected_output

def test_resolve_deps_single_package():
    file_name = "single_package_deps"
    file_path = get_data_file_path(f'{file_name}.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    output = capture_stdout(resolve_deps, data)
    expected_output = load_expected_output(f'{file_name}.txt')
    assert output == expected_output

# ------------ Errors related to json and the data itself ------------

def test_resolve_deps_missing_dependency():
    file_name = "missing_deps"
    file_path = get_data_file_path(f'{file_name}.json')
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
