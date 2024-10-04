"""
TODO: design me? -- probably need to make object oriented as cli expands
"""
import os
from datetime import datetime
from pathlib import Path

import click

from pydiatr.cli.templates.templates import template_env


def create_registry(ctx, name: str, project_root_dir: str, output_dir: str, overwrite: bool):
    param_string = " ".join([f"--{k} {v}" for k, v in ctx.params.items()])
    command_used = f"pydiatr {ctx.command_path} {param_string}"

    module_name = name.lower()

    if not os.path.isdir(project_root_dir):
        click.echo(f"Invalid project root directory: {project_root_dir}")
        return
    project_root_path = Path(project_root_dir).resolve()
    click.echo(f"Project root directory: {project_root_path}")

    if not os.path.isdir(output_dir):
        click.echo(f"Invalid output directory: {output_dir}")
        return
    output_path = Path(output_dir).resolve()

    registry_file = output_path / f"{module_name}_registry.py"

    if registry_file.exists() and not overwrite:
        click.echo(f"Registry file already exists: {registry_file}")
        return

    output_path_relative_root = os.path.relpath(output_path, project_root_path)
    root_import = f"{project_root_path.name}{output_path_relative_root.replace('/', '.').lstrip('.')}"

    template = template_env.get_template("registry_template.py.jinja2")
    rendered = template.render(module_name=module_name, root_import=root_import, timestamp=datetime.now().isoformat(), command_used=command_used)

    os.makedirs(output_path, exist_ok=True)
    with open(registry_file, "w") as f:
        f.write(rendered)
    click.echo(f"Registry file created: {registry_file}")
