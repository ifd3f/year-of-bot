#!/usr/bin/env python

import asyncio
import os
import random

from datetime import datetime

import data

from pleroma import Pleroma


def generate_prediction():
    today = datetime.now()
    y = random.randint(today.year, today.year + 25)
    p_template = random.choice(data.predictions)

    fmt_dict = {
        f's{i}': random.choice(data.subjects)
        for i in range(1, 10)
    }
    fmt_dict['s'] = random.choice(data.subjects)

    prediction = p_template.format(**fmt_dict)

    return f'{y} will be the year of {prediction}'


async def main():
    prediction = generate_prediction()
    print(prediction)

    server_url = os.environ["SERVER_URL"]
    access_token = os.environ["ACCESS_TOKEN"]
    async with Pleroma(api_base_url=server_url, access_token=access_token) as pl:
        await pl.post(prediction, visibility='unlisted')


if __name__ == '__main__':
    asyncio.run(main())

