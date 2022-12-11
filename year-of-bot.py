#!/usr/bin/env python

import asyncio
import os
import random

from datetime import datetime
from pathlib import Path

from pleroma import Pleroma


DATA_DIR = Path(__file__).parent

with (DATA_DIR / 'os.txt').open() as f:
    oses = [
        l.strip() for l in f
        if not l.isspace()
    ]

with (DATA_DIR / 'platform.txt').open() as f:
    platforms = [
        l.strip() for l in f
        if not l.isspace()
    ]


def generate_prediction():
    today = datetime.now()
    y = random.randint(today.year, today.year + 25)
    o = random.choice(oses)
    p = random.choice(platforms)
    return f'{y} will be the year of {o} {p}'


async def main(access_token, server_url):
    async with Pleroma(api_base_url=server_url, access_token=access_token) as pl:
        await pl.post(generate_prediction(), visibility='unlisted')


if __name__ == '__main__':
    SERVER_URL = os.environ["SERVER_URL"]
    ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]

    asyncio.run(main(ACCESS_TOKEN, SERVER_URL))

