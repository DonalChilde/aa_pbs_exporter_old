"""
A entrypoint for cli programs that provides some standard capabilities.

[extended_summary]
TODO multi level verbose, store in ctx
TODO App config, loaded from app dir
"""

from logging import Logger

import click

from aa_pbs_exporter.cli.pypdf4_cli import pypdf4_

logger = Logger(__name__)


class App:
    def __init__(self, config, verbosity: int = 0) -> None:
        self.verbosity = verbosity
        self.config = config


@click.group()
@click.option("-v", "--verbose")
@click.pass_context
def main(ctx: click.Context, verbose):
    ctx.obj = App({}, 0)
    return 0


main.add_command(pypdf4_)
