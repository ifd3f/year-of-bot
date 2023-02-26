import asyncio
import os
import sys

import asyncclick as click

from pleroma import Pleroma

from . import generate_fmt_dict, generate_prediction, data


def main():
    asyncio.run(cli())


@click.group()
async def cli():
    """
    A Pleroma bot that predicts what the future of technology holds.
    """


@cli.command()
@click.option(
    "-d",
    "--dry-run",
    is_flag=True,
    default=False,
    help="Generate and print a prediction, but do not actually post.",
)
async def post(dry: bool):
    """
    Send a post. If --dry-run, is not enabled, then you should provide SERVER_URL
    and ACCESS_TOKEN environment variables.
    """
    prediction = generate_prediction()
    print(prediction)

    if dry:
        return 0

    server_url = os.environ["SERVER_URL"]
    access_token = os.environ["ACCESS_TOKEN"]
    async with Pleroma(api_base_url=server_url, access_token=access_token) as pl:
        await pl.post(prediction, visibility="unlisted")


@cli.command()
def verify():
    """
    Verify that all of this file's data strings are valid.
    """
    d = generate_fmt_dict()
    for g in data.predictions:
        for t in g:
            t.format(**d)
    print("All predictions are OK", file=sys.stderr)


if __name__ == "__main__":
    main()
