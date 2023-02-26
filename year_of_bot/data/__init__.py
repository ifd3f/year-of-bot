from pathlib import Path


data_dir = Path(__file__).parent

with (data_dir / "subjects.txt").open() as f:
    subjects = [l.strip() for l in f if not l.isspace()]

predictions = []
for file in (data_dir / "predictions").glob("*.txt"):
    with file.open() as f:
        predictions.append([l.strip() for l in f if not l.isspace()])
