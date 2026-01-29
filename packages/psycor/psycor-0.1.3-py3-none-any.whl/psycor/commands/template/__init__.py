import click
from save import save

@click.group()
def template():
    pass

template.add_command(save)