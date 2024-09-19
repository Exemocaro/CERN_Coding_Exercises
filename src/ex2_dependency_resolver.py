import json
import sys
import os
from typing import Dict, List, Optional

def pprint(d: Dict[str, List[str]]) -> None:
    """
    Pretty print a dictionary.
    Used in this file to check if the json was loaded correctly.

    Args:
        d (Dict[str, List[str]]): The dictionary to print.

    Returns:
        None
    """
    print(json.dumps(d, sort_keys=True, indent=4))

def load_deps(file_path: str) -> Dict[str, List[str]]:
    """
    Loads the dependencies from a json file.

    Args:
        file_path (str): The path to the JSON file containing dependencies.

    Returns:
        Dict[str, List[str]]: A dictionary where keys are package names and values are lists of dependencies.

    Raises:
        FileNotFoundError: If the specified file is not found.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    with open(file_path, 'r') as f:
        return json.load(f)

def resolve_deps(deps: Dict[str, List[str]], pckgs: Optional[List[str]] = None, seen: Optional[set] = None, depth: int = 0) -> None:
    """
    This function essentially resolves dependencies using a recursive depth-first search (DFS) approach.
    The graph is represented as a dictionary where the key is the package name and the values are lists of dependencies.
    The optional arguments are optional because in the first call of the function they are not needed, 
    as they are set to the loaded \"deps\" dictionary with no previous \"pckgs\" or \"seen\" packages, and with a \"depth\" of 0.

    Args:
        deps (Dict[str, List[str]]): The dependency graph to resolve.
        pckgs (Optional[List[str]]): The current list of packages to process. If None, use all keys in deps.
        seen (Optional[set]): Set of packages that have been processed to avoid cycles.
        depth (int): The current depth in the dependency tree, used for indentation of the print statements.

    Returns:
        None

    Raises:
        TypeError: If a package name is not a string or if dependencies are not in a list.

    Example:
        >>> deps = {
        ...     "pkg1": ["pkg2", "pkg3"],
        ...     "pkg2": ["pkg3"],
        ...     "pkg3": []
        ... }
        >>> resolve_deps(deps)
        -pkg1
          -pkg2
            -pkg3
          -pkg3
        -pkg2
          -pkg3
        -pkg3
    """

    # steps:
    # loop through deps.keys() and print the "main" packages
    # do dfs on the dependencies of each pckg, and recursively call the function with the current package's list of dependencies
    # go on until all nodes are on the seen set.

    # these 2 ifs were not set before as there were 2 functions here.
    # now I need these checks to see if it's the "first"/"main" time running the loop.
    if pckgs is None:
        pckgs = list(deps.keys())

    if seen is None:
        seen = set()
    
    for pckg in pckgs:
        if not isinstance(pckg, str):  # without this check, it would loop over the chars of the string!
            raise TypeError(f"Package name must be a string, not {type(pckg)}")
        
        if pckg not in seen:
            print(f"{(depth*2) * " "}-{pckg}")
            seen.add(pckg) # added to avoid circular dependencies inside this own dependencies' list!
            if isinstance(deps[pckg], list):  # checking if the dependencies of the current package are a list, as expected
                resolve_deps(deps, deps[pckg], seen.copy(), depth + 1) # i use seen.copy() to avoid modifying the seen set for the other branches
            else:
                raise TypeError(f"Dependencies of {pckg} must be a list, not {type(deps[pckg])}")

def main():
    """
    Main function to run the dependency resolver.
    You can test it with pytest, but if you want to test a specific thing you can run it directly here as well.

    Usage:
        python -m src.ex2_dependency_resolver <path_to_json_file>

    Returns:
        None

    Raises:
        SystemExit: If the correct number of command-line arguments is not provided.
    """
    if len(sys.argv) != 2:
        print("Usage: python -m src.ex2_dependency_resolver <path_to_json_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        deps = load_deps(file_path)
        print("Loaded dependencies:")
        pprint(deps)
        print("\nResolved dependency tree:")
        resolve_deps(deps)

        # check if the file with the expected output exists, and if so print it
        expected_output_path = os.path.splitext(file_path)[0] + '.txt'
        if os.path.exists(expected_output_path):
            print("\nExpected output:")
            with open(expected_output_path, 'r') as f:
                print(f.read())
        else:
            print("\nNo expected output file found.")

    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file: {file_path}")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing dependency in the graph: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
