from .cli import prevsession


def register(cli):
    cli.add_command(prevsession, name="ps")
