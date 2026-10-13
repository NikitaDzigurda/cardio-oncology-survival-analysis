"""Explicitly execute the research notebooks; never run during project assembly."""
from pathlib import Path
import argparse
import os
import sys
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from cardio_oncology.paths import project_paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--step", choices=["01", "02", "all"], default="02")
    parser.add_argument("--kernel", default="cardio-oncology")
    args = parser.parse_args()
    paths = project_paths(ROOT)
    paths.run.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(paths.run / ".matplotlib"))
    names = ["01_prepare_data.ipynb", "02_survival_analysis.ipynb"]
    for name in names:
        if args.step != "all" and not name.startswith(args.step):
            continue
        path = ROOT / "notebooks" / name
        notebook = nbformat.read(path, as_version=4)
        print("Executing:", name, flush=True)
        client = NotebookClient(notebook, timeout=None, kernel_name=args.kernel,
                                resources={"metadata": {"path": str(ROOT)}})
        try:
            client.execute()
        finally:
            nbformat.write(notebook, paths.run / name)
        print("Saved locally:", (paths.run / name).relative_to(ROOT), flush=True)


if __name__ == "__main__":
    main()
