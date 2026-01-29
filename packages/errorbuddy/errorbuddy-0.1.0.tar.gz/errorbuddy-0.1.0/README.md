Versioning Strategy
	•	0.1.0 → First public release
	•	0.2.0 → More errors added
	•	1.0.0 → Stable + AI support

## CLI Usage 🚀
Run any Python file and get human-readable errors:

```bash

# Structure

easyerrors myfile.py

easyerrors/
│
├── easyerrors/
│   ├── init.py
│   ├── explainer.py
│   ├── rules.py
│   └── cli.py   👈 NEW
│
├── tests/
│   └── test_basic.py
│
├── pyproject.toml
├── README.md

##  Build Package

```bash
pip install build twine
python -m build