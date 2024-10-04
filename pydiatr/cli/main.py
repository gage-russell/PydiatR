import click

from pydiatr.cli.callables import handler_callables, registry_callables


@click.group()
def cli():
    pass


@cli.group()
def handler():
    pass


@handler.command()
@click.option("--option", "-o", type=click.Choice(handler_callables.HANDLER_CREATE_OPTIONS), prompt=True)
@click.option("--name", "-n", type=str, prompt=True)
@click.option("--project_root_dir", "-p", type=click.Path(exists=True), default="./", prompt=True)
@click.option("--registry_module_file", "-r", type=click.Path(exists=True), default="./registry.py", prompt=True)
@click.option("--output_dir", "-d", type=click.Path(), default="./handlers", prompt=True)
@click.option("--overwrite", "-w", default=False, is_flag=True, prompt=True)
@click.pass_context
def create_handler(ctx, option: str, name: str, project_root_dir: str, registry_module_file: str, output_dir: str, overwrite: bool):
    handler_callables.create_handler(ctx, name, option, project_root_dir, registry_module_file, output_dir, overwrite)


@cli.group()
def registry():
    pass


@registry.command()
@click.option("--name", "-n", type=str, prompt=True)
@click.option("--project_root_dir", "-p", type=click.Path(exists=True), default="./", prompt=True)
@click.option("--output_dir", "-d", type=click.Path(), default="./", prompt=True)
@click.option("--overwrite", "-w", default=False, is_flag=True, prompt=True)
@click.pass_context
def create_registry(ctx, name: str, project_root_dir: str, output_dir: str, overwrite: bool):
    registry_callables.create_registry(ctx, name, project_root_dir, output_dir, overwrite)
