import os
import shutil
from os.path import join

import click

from playrix.parse import DirectoryParser
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
            raise click.FileError(
                output, hint='folder exists and is not empty.')
    else:
        os.makedirs(output)

    padding = len(str(number))
    template = '{i:0%dd}.zip' % padding
    for i in range(number):
        archive_name = template.format(i=i)
        click.echo(f'Generating archive: {archive_name}')
        filename = join(output, archive_name)
        archive = RandomArchive(filename)
        try:
            archive.build()
        except FileExistsError:
            click.echo(f'Warning! Archive already exists: {filename}')
        except Exception as e:
            click.echo(f'Unexpected error: {str(e)}')
            raise click.Abort(1)

    click.echo(f'Archives generated: {output}')


@cli.command()
@click.argument('input-dir', type=click.Path(file_okay=False))
@click.argument('output-dir', type=click.Path(file_okay=False))
@click.option('--n-jobs', type=int, default=None)
@click.option('--rewrite/--no-rewrite', is_flag=True)
def parse(input_dir, output_dir, n_jobs, rewrite):
    """
    Parses directory with XML archives.
    """
    output_dir = os.path.abspath(output_dir)

    if not os.path.exists(input_dir):
        raise click.FileError(f'"{input_dir}"', hint='does not exist')

    if os.path.exists(output_dir):
        if len(os.listdir(output_dir)) > 0 and not rewrite:
            raise click.FileError(
                f'"{output_dir}"', hint='folder exists and is not empty.')
        if rewrite:
            shutil.rmtree(output_dir)
            os.makedirs(output_dir)
    else:
        os.makedirs(output_dir)

    click.echo(f'Parsing archives from the folder: {input_dir}')
    parser = DirectoryParser(input_dir)
    result = parser.parse(num_of_workers=n_jobs)

    meta_path = join(output_dir, 'levels.csv')
    objects_path = join(output_dir, 'objects.csv')

    result.meta.to_csv(meta_path, index=False)
    result.objects.to_csv(objects_path, index=False)

    click.echo(f'Meta data saved: {meta_path}')
    click.echo(f'Objects data saved: {objects_path}')


if __name__ == '__main__':
    cli()
