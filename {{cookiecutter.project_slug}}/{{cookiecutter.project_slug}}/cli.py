import sys
import click


@click.command()
def main(args=None):
    """TODO document your CLI tool"""
    click.echo("See click documentation at http://click.pocoo.org/")


if __name__ == "__main__":
    # this is normally never executed, the CLI will actually be called via setuptools
    sys.exit(main())  # pragma: no cover
