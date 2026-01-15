import typer
from typing_extensions import Annotated
from pathlib import Path
import package.config.init as cfg


cfg_file: str = None

app = typer.Typer(help="fflow")


@app.callback()
def initialize(
    ctx: typer.Context,
    config: Annotated[
        Path,
        typer.Option(
            "--config",
            "-c",
            help="config file (default is $HOME/.double-entry-generator.yaml)",
        ),
    ] = Path.home()
    / "fflow.yaml",
    toogle: Annotated[
        bool, typer.Option("--toggle", "-t", help="Help message for toggle")
    ] = False,
):

    if ctx.invoked_subcommand == "version":
        return
    global cfg_file
    cfg_file = str(config)
    cfg.init_config(cfg_file)


@app.command()
def version():
    print("bflow: 1.0.0")
