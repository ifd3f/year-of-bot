#!/usr/bin/env python

import asyncio
import os
import random
import sys

from datetime import datetime

import click

from pleroma import Pleroma

from . import data


def generate_prediction():
    today = datetime.now()
    y = random.randint(today.year, today.year + 25)
    p_template = random.choice(random.choice(data.predictions))

    fmt_dict = generate_fmt_dict()

    prediction = p_template.format(**fmt_dict)

    return f"{y} will be the year of {prediction}"


def main():
    asyncio.run(async_main())


async def async_main():
    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        verify_data()
        return

    prediction = generate_prediction()
    print(prediction)

    server_url = os.environ["SERVER_URL"]
    access_token = os.environ["ACCESS_TOKEN"]
    async with Pleroma(api_base_url=server_url, access_token=access_token) as pl:
        await pl.post(prediction, visibility="unlisted")


def verify_data():
    d = generate_fmt_dict()
    for g in data.predictions:
        for t in g:
            t.format(**d)
    print("All predictions are OK")


def generate_fmt_dict():
    fmt_dict = {f"s{i}": random.choice(data.subjects) for i in range(1, 10)}
    fmt_dict["s"] = random.choice(data.subjects)

    return fmt_dict


if __name__ == "__main__":
    main()
