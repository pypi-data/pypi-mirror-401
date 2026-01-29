import typer
from typing_extensions import Annotated
from package.compiler.task import add_task
from package.cmd.root import app


@app.command()
def read(
    config: Annotated[str, typer.Option("--config", "-c", help="config file")] = "",
):
    add_task(config)
