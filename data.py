from pathlib import Path


data_dir = Path(__file__).parent

with (data_dir / 'subjects.txt').open() as f:
    subjects = [
        l.strip() for l in f
        if not l.isspace()
    ]

with (data_dir / 'predictions.txt').open() as f:
    predictions = [
        l.strip() for l in f
        if not l.isspace()
    ]

