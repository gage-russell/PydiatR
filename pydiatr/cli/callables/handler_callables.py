"""
TODO: design me? -- probably need to make object oriented as cli expands
"""
import importlib
import inspect
import os
from datetime import datetime
from pathlib import Path

import click

from pydiatr.cli.templates.templates import template_env
from pydiatr.registry import Registry

HANDLER_CREATE_OPTIONS = ["command", "query"]


def create_handler(ctx, name, option, project_root_dir, registry_module_file, output_dir, overwrite: bool):
    param_string = " ".join([f"--{k} {v}" for k, v in ctx.params.items()])
    command_used = f"pydiatr {ctx.command_path} {param_string}"

    if option.lower() == "command":
        suffix = "Command"
    elif option.lower() == "query":
        suffix = "Query"
    else:
        click.echo(f"Invalid option. Expected one of: {HANDLER_CREATE_OPTIONS}")
        return

    module_name = name.lower()
    class_name = module_name.replace("_", " ").title().replace(" ", "")
    module_full_name = f"{module_name}_{option.lower()}"
    timestamp = datetime.now().isoformat()

    # ensure project_root_dir is a directory
    if not os.path.isdir(project_root_dir):
        click.echo(f"Invalid project root directory: {project_root_dir}")
        return
    project_root_path = Path(project_root_dir).resolve()
    click.echo(f"Project root directory: {project_root_path}")

    # ensure registry_module_file is a file
    if not os.path.isfile(registry_module_file):
        click.echo(f"Invalid registry module file: {registry_module_file}")
        return
    registry_module_file = Path(registry_module_file).resolve()
    click.echo(f"Registry module file: {registry_module_file}")

    registry_relative_path = os.path.relpath(registry_module_file, project_root_path)

    registry_part_import = registry_relative_path.replace(".py", "").replace("/", ".").lstrip(".")
    registry_root_import = project_root_path.name
    registry_import = f"{registry_root_import}.{registry_part_import}"
    click.echo(f"Registry module import: {registry_import}")
    try:
        click.echo(f"Importing registry module {registry_import}")
        registry_module = importlib.import_module(registry_import)
    except ImportError:
        click.echo(f"Error importing registry module {registry_module_file}. Ensure this is a relative path and is a sub folder of the current directory.")
        return
    for name, obj in inspect.getmembers(registry_module):
        if issubclass(type(obj), Registry):
            registry_class = name
            break
    else:
        click.echo(f"No Registry class found in {registry_module_file}")
        return

    template = template_env.get_template("handler_template.py.jinja2")
    output = template.render(
        module_name=module_full_name,
        timestamp=timestamp,
        command_used=command_used,
        registry_module=registry_import,
        registry_class=registry_class,
        class_name=class_name,
        class_suffix=suffix,
    )
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, f"{module_full_name}.py")
    if os.path.exists(output_file_path) and not overwrite:
        click.echo(f"File {output_file_path} already exists. Use --overwrite flag to overwrite.")
        return
    with open(output_file_path, "w") as f:
        f.write(output)
    click.echo(f"Module {module_full_name} generated successfully at {output_file_path}")
