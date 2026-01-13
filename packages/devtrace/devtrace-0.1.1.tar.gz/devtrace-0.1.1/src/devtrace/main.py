import typer
from devtrace import commands

app = typer.Typer(
    name="devtrace",
    help="A CLI work logger.",
    no_args_is_help=True
)

app.command()(commands.init)
app.command()(commands.log)
app.command()(commands.see)
app.command()(commands.view)
app.command()(commands.help)

if __name__ == "__main__":
    app()