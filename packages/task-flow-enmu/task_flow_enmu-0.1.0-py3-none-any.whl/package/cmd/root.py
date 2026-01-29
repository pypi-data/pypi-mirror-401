import typer

app = typer.Typer(help="tflow")


def version_callback(value: bool):
    if value:
        print("Awesome CLI Version: 1.0.0")
        raise typer.Exit()


@app.callback()
def main(
    # 将参数挂载到 callback 中
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
    verbose: bool = typer.Option(False, "--verbose", help="Enable verbose output"),
):
    """
    这是根命令的帮助文档。
    """
    if verbose:
        print("Verbose mode is ON")
