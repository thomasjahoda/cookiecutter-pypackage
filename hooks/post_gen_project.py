import os
import subprocess
import tempfile
from pathlib import Path

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def initialize_git_repository():
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "add", "-A", "."], check=True)
    subprocess.run(["git", "commit", "-m", "generated project from template {{ cookiecutter._template }}"], check=True)
    subprocess.run(["git", "branch", "cookiecutter-template"], check=True)


def initialize_venv_using_virtualenvwrapper():
    bash_script_fd, bash_script_file_str = tempfile.mkstemp(suffix="create_venv_using_virtualenvwrapper.sh")
    bash_script_file = Path(bash_script_file_str)
    bash_script = """source ~/.bashrc
source $VIRTUALENVWRAPPER_SCRIPT
mkvirtualenv "{{ cookiecutter.project_slug }}" || exit 1
"""
    bash_script_file.write_text(bash_script, encoding="utf-8")
    bash_script_file.chmod(0o700)
    print("Going to execute the following bash script to initialize the venv using virtualenvwrapper:\n" + bash_script)

    subprocess.run(["bash", str(bash_script_file)], check=True)


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

    if '{{ cookiecutter.initialize_venv_using_virtualenvwrapper }}' == 'y':
        initialize_venv_using_virtualenvwrapper()
