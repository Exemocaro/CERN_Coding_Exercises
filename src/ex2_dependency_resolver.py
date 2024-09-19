import json
import sys
from typing import Dict, List

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

def dfs(deps: Dict[str, List[str]], pckgs: List[str], seen: set, depth: int) -> None:
    """
    Depth first search function to resolve the dependencies.

    Args:
        deps (Dict[str, List[str]]): The full dependency graph.
        pckgs (List[str]): The current list of packages to process.
        seen (set): Set of packages that have been processed to avoid cycles.
        depth (int): The current depth in the dependency tree, used for indentation of the print statements.

    Returns:
        None
    """

    for pckg in pckgs:
        if pckg not in seen:
            print(f"{(depth*2) * " "}-{pckg}")
            seen.add(pckg)
            if isinstance(deps[pckg], list):  # checking if the dependencies of the current package are a list, as expected
                dfs(deps, deps[pckg], seen.copy(), depth + 1) # i use seen.copy() to avoid modifying the seen set for the other branches
            else:
                raise TypeError(f"Dependencies of {pckg} must be a list, not {type(deps[pckg])}")

def resolve_deps(deps: Dict[str, List[str]]) -> None:
    """
    This function is essentially a DFS over the dependencies graph.
    The graph will be represented as a dictionary (the loaded json) where the key is the package name.

    Args:
        deps (Dict[str, List[str]]): The dependency graph (dict) to resolve.

    Returns:
        None
    """

    # steps:
    # loop through deps.keys() and print the "main" packages
    # do dfs on the dependencies of each pckg, and recursively call the function with the current package's list of dependencies
    # go on until all nodes are on the seen set.
    
    seen = set()
    for pckg in deps.keys():
        if not isinstance(pckg, str):  # without this check, it would loop over the chars of the string!
            raise TypeError(f"Package name must be a string, not {type(pckg)}")
        print(f"-{pckg}")
        seen.add(pckg) # added to avoid circular dependencies inside this own dependencies' list!
        if isinstance(deps[pckg], list):  # checking if the dependencies of the current package are a list, as expected
            dfs(deps, deps[pckg], seen.copy(), 1)
        else:
            raise TypeError(f"Dependencies of {pckg} must be a list, not {type(deps[pckg])}")

def main():
    """
    Main function to run the dependency resolver.

    This function:
    1. Checks if a file path is provided as a command-line argument.
    2. Loads the dependencies from the specified JSON file.
    3. Pretty prints the loaded dependencies.
    4. Resolves and prints the dependency tree.

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
