import typer
from package.cmd.root import app
from typing_extensions import Annotated
from package.hooks.todo_process import update_file
from pathlib import Path


home = Path.home()


config_path = home / ".flow" / "task.yaml"


@app.command()
def modify(
    new_json: Annotated[str, typer.Option("--arg", "-a", help="new data")] = "",
    command: Annotated[str, typer.Option("--cmd", "-c", help="command")] = "",
    config: Annotated[
        str, typer.Option("--config", "-cf", help="config")
    ] = config_path,
):
    update_file(new_json, command, config)
