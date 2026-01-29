def main():
    import sys
    import runpy
    from errorbuddy.explainer import explain

    if len(sys.argv) < 2:
        print("Usage: errorbuddy <python_file.py>")
        sys.exit(1)

    try:
        runpy.run_path(sys.argv[1], run_name="__main__")
    except Exception as e:
        explain(e)