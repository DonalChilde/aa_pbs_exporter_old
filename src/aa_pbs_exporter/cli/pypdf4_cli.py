from pathlib import Path

import click

from aa_pbs_exporter.app_lib import pypdf4_util


@click.group(name="pypdf4")
@click.pass_context
def pypdf4_(ctx: click.Context):
    pass


@click.command(name="page-count")
@click.argument(
    "file_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    required=True,
)
@click.pass_context
def page_count_(ctx: click.Context, file_path: Path):
    page_count = pypdf4_util.page_count(file_path)
    click.echo(f"The pdf file at {file_path} has {page_count} pages.")


@click.command()
@click.argument(
    "file_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    required=True,
)
@click.option("-s", "--start-page", type=int, default=0)
@click.option("-e", "--end-page", type=int, default=-1)
@click.pass_context
def export_text(ctx: click.Context, file_path: Path, start_page: int, end_page: int):
    try:
        for page in pypdf4_util.text_pages(file_path, start_page, end_page):
            click.echo(page.page_text)
    except FileNotFoundError as ex:
        raise click.BadParameter(f"{file_path} is not a valid path.")
    except ValueError as ex:
        raise click.BadParameter(f"{ex}")


pypdf4_.add_command(page_count_)
pypdf4_.add_command(export_text)
