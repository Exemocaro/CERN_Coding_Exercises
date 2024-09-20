# CERN Coding Exercises

Author: Mateus Pereira

The coding exercises and my solutions to them for the TE-MPE-PE Section at CERN.

## Introduction and Thoughts

Each exercise file is inside the src folder and the tests for each exercise are inside the tests folder with the same name as the exercise file, but with the prefix "test_". I wrote tests for the both of them using pytest to ensure the correctness of the functions, and because I believe that writing tests is a good practice to ensure the quality of the code. 

To make the second exercise pip installable, I ended up making both of them pip installable using a pyproject.toml. I could have use a setup.py, but the .toml approach is [the long term recommended solution](https://packaging.python.org/en/latest/discussions/setup-py-deprecated/#is-pyproject-toml-mandatory) while setup.py is being slowly deprecated.

For the CI pipeline I used Github Actions. To ensure the "best possible automation for the quality" of the code, I added a job to run the tests and another for a linter, which is pylint. I'm not sure if there was more I could have added here since I'm not very experienced with CI/CD pipelines yet, but I think that this is a good start.

All in all I probably overengineered the solution and overthought most of the stuff I had to write. Maybe I could have written a simpler solution for both exercises, but I wanted to make sure I was writing good code, following best practices and displaying my skills.

### First Exercise

As for the 1st exercise, it was pretty straightforward to implement the function that detects duplicates in a list of elements. I used the Counter class from the collections module to count the occurrences of each element in the list and then I returned a list with the elements that have more than one occurrence. After implementing a simple version and testing it, I changed it a bit and added a set to check if an element was already added to the list of duplicates in order to massively improve the time on the tests.

### Second Exercise

For the 2nd exercise, I decided to go with a DFS approach. As I tested the function with different json files, I realized that the order could matter depending on the way I coded it. For example, if this were a package manager and it was installing each package in the order they appeared, we wouldn't want to install the same package twice. So, with this strategy, the following json file:

```json
{
  "pkg1": ["pkg2", "pkg3"],
  "pkg2": ["pkg3"],
  "pkg3": []
}
```

would result in the following order of packages:
```
-pkg1
  -pkg2
    -pkg3
  -pkg3
-pkg2
  -pkg3
-pkg3
```

while this one:
  
```json
{
  "pkg1": ["pkg3", "pkg2"],
  "pkg2": ["pkg3"],
  "pkg3": []
}
```

would result in:
```
-pkg1
  -pkg3
  -pkg2
-pkg2
  -pkg3
-pkg3
```

Notice how the pkg3 is installed before pkg2 in the first case and after in the second case. As such, the pkg2 looks like it has no dependencies. 

But since the point of the exercise is to "reconstruct the full dependency graph", i had to write it in a way that the order of the packages doesn't matter. For that, when checking for each dependency of a package, I added it to a "seen" list. That list couldn't be the same for each branch, so I used the copy() method to solve that.


## Environment Setup

- Python version: 3.12.1

To set up the project:

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - On Windows (PowerShell):
     ```
     .\.venv\Scripts\Activate.ps1
     ```
   - On Windows (Command Prompt):
     ```
     .\.venv\Scripts\activate.bat
     ```
   - On Unix or MacOS:
     ```
     source .venv/bin/activate
     ```
4. Install the project (in editable mode):
   ```
   pip install -e .
   ```
   Or, in standard mode:
   ```
   pip install .
   ```

   Editable mode (-e) is recommended for development as it allows you to modify the source code without reinstalling the package. Standard mode is suitable for production use.


## Running the Exercises

After installing the project with pip, you can simply write in your console the following commands to run the exercises:

For the first exercise (duplicate detector): You'll be prompted to enter a list of elements to test the function.

```
ex1
```

For the second exercise (dependency resolver):
```
ex2 path/to/json
```

Example:
```
ex2 data/simple_deps1.json
```


## Running Tests

To run the tests for each exercise:

```
pytest tests/test_ex1_duplicate_detector.py
pytest tests/test_ex2_dependency_resolver.py
```

## Running Linter

You don't need to do this, but since pylint is installed with the project you can test the linter to see the result before pushing into the main branch. You should also install the pylint extension if you use VSCode, for example. 

Anyway, to run the linter on the source files (you can do the same for the tests, just write the path to the tests folder instead of the src folder):

```
pylint src
```

## CI Pipeline

This project uses GitHub Actions for continuous integration. The CI pipeline runs tests and linting on every push to the main branch and on every pull request to the main branch. You can view the CI configuration in `.github/workflows/ci.yaml`.
