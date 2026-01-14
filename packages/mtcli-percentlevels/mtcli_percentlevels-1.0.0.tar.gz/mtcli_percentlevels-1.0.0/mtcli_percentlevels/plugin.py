from .cli import percentlevels


def register(cli):
    cli.add_command(percentlevels, name="pl")
