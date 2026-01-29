import sys
import runpy
from easyerrors.explainer import explain

def main():
    if len(sys.argv) < 2:
        print("Usage: easyerrors <python_file.py>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        runpy.run_path(file_path, run_name="__main__")
    except Exception as e:
        explain(e)