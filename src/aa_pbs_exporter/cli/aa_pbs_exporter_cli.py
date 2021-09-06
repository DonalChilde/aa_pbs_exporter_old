"""Console script entry point for aa_pbs_exporter."""

import sys
from logging import Logger

import click

# from aa_pbs_exporter.app_config import LOGGER
from aa_pbs_exporter.cli.example import hello

logger = Logger(__name__)


@click.group()
@click.pass_context
def main(ctx: click.Context, args=None):
    """Console script for aa_pbs_exporter."""
    # NOTE: as written, this code only runs when hello is called,
    # not when <entry point> --help is called. This is a group to
    # hold other commands and groups.
    ctx.obj = {}
    ctx.obj["important_value"] = {"key": "oh so important"}
    click.echo(
        "Replace this message by putting your code into " "aa_pbs_exporter.cli.main"
    )
    click.echo(args)
    click.echo("See click documentation at https://click.palletsprojects.com/")
    logger.error("Just checking!")
    return 0


main.add_command(hello)
