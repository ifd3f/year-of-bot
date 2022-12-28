#!/usr/bin/env python

import asyncio
import os
import random

from datetime import datetime
from pathlib import Path

from pleroma import Pleroma


DATA_DIR = Path(__file__).parent

with (DATA_DIR / 'subjects.txt').open() as f:
    SUBJECTS = [
        l.strip() for l in f
        if not l.isspace()
    ]

with (DATA_DIR / 'predictions.txt').open() as f:
    PREDICTIONS = [
        l.strip() for l in f
        if not l.isspace()
    ]


def generate_prediction():
    today = datetime.now()
    y = random.randint(today.year, today.year + 25)
    p = random.choice(PREDICTIONS)

    fmt_dict = {
        f's{i}': random.choice(SUBJECTS)
        for i in range(1, 10)
    }
    fmt_dict['s'] = random.choice(SUBJECTS)

    pred = p.format(**fmt_dict)

    return f'{y} will be the year of {pred}'


async def main():
    prediction = generate_prediction()
    print(prediction)

    server_url = os.environ["SERVER_URL"]
    access_token = os.environ["ACCESS_TOKEN"]
    async with Pleroma(api_base_url=server_url, access_token=access_token) as pl:
        await pl.post(prediction, visibility='unlisted')


if __name__ == '__main__':
    asyncio.run(main())

