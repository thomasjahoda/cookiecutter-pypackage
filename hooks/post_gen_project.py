import os
import subprocess

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def initialize_git_repository():
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "add", "-A", "."], check=True)
    subprocess.run(["git", "commit", "-m", "generated project from template {{ cookiecutter._template }}"], check=True)
    subprocess.run(["git", "branch", "cookiecutter-template"], check=True)


if __name__ == '__main__':

    if '{{ cookiecutter.create_author_file }}' != 'y':
        remove_file('docs/authors.rst')

    if '{{ cookiecutter.use_pytest }}' == 'y':
        remove_file('tests/__init__.py')

    if 'no' in '{{ cookiecutter.command_line_interface|lower }}':
        cli_file = os.path.join('{{ cookiecutter.project_slug }}', 'cli.py')
        remove_file(cli_file)
        cli_bash_autocomplete_file = os.path.join('dev-util', 'bash_autocomplete.sh')
        remove_file(cli_bash_autocomplete_file)

    if 'Not open source' == '{{ cookiecutter.open_source_license }}':
        remove_file('LICENSE')

    if '{{ cookiecutter.initialize_git_repository }}' == 'y':
        initialize_git_repository()
