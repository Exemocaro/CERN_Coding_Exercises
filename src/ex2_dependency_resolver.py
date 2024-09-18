import json
import sys
from typing import Dict, List

def load_dependencies(file_path: str) -> Dict[str, List[str]]:
    with open(file_path, 'r') as f:
        return json.load(f)

deps = load_dependencies(sys.argv[1])
print(deps)
