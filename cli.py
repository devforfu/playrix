import os

import click

from playrix.generate import RandomArchive


@click.group()
def cli():
    pass


@cli.command()
@click.argument('number', type=int)
@click.argument('output', type=str)
def generate(number, output):
    """
    Creates a collection of random ZIP archives.
    """
    output = os.path.abspath(output)

    if os.path.exists(output):
        if len(os.listdir(output)) > 0:
            raise click.FileError(f'folder exists and not empty: {output}')

    os.makedirs(output)

    padding = len(str(number))
    template = '{i:0%dd}.zip' % padding
    for i in range(number):
        filename = os.path.join(output, template.format(i=i))
        archive = RandomArchive(filename)
        try:
            archive.build()
        except FileExistsError:
            click.echo(f'Warning! Archive already exists: {filename}')
        except Exception as e:
            click.echo(f'Unexpected error: {str(e)}')
            raise click.Abort(1)

    click.echo(f'Archives generated: {output}')


if __name__ == '__main__':
    cli()
