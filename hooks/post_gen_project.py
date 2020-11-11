import os
import subprocess
import tempfile
from pathlib import Path

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def initialize_git_repository_if_necessary():
    create_git_repository = not Path(".git").exists()
    if create_git_repository:
        print("Initializing Git repository")
        subprocess.run(["git", "init"], check=True)

        print("Setting git config user.name and user.email with provided settings")
        subprocess.run(["git", "config", "user.name", "{{ cookiecutter.full_name.replace('\"', '\\\"') }}"], check=True)
        subprocess.run(["git", "config", "user.email", "{{ cookiecutter.email }}"], check=True)

        print(f"Committing initial files")
        subprocess.run(["git", "add", "-A", "."], check=True)
        subprocess.run(["git", "commit", "-m", "generated project from template {{ cookiecutter._template }}"],
                       check=True)


def initialize_venv_using_virtualenvwrapper():
    bash_script_fd, bash_script_file_str = tempfile.mkstemp(suffix="create_venv_using_virtualenvwrapper.sh")
    bash_script_file = Path(bash_script_file_str)
    bash_script = """source ~/.bashrc
source $VIRTUALENVWRAPPER_SCRIPT
VENV_NAME="{{ cookiecutter.project_slug }}"
if echo "$(lsvirtualenv)" | grep -q -F "${VENV_NAME}"; then 
    echo "venv $VENV_NAME already exists"
else
    echo "Creating venv"
    mkvirtualenv "$VENV_NAME" || exit 1
fi
"""
    bash_script_file.write_text(bash_script, encoding="utf-8")
    bash_script_file.chmod(0o700)
    print("Going to execute the following bash script to initialize the venv using virtualenvwrapper:\n" + bash_script)

    subprocess.run(["bash", str(bash_script_file)], check=True)


if __name__ == '__main__':

    if '{{ cookiecutter.create_author_file }}' != 'y':
        remove_file('docs/authors.rst')

    if 'no' in '{{ cookiecutter.command_line_interface|lower }}':
        cli_file = os.path.join('{{ cookiecutter.project_slug }}', 'cli.py')
        remove_file(cli_file)
        cli_bash_autocomplete_file = os.path.join('dev-util', 'bash_autocomplete.sh')
        remove_file(cli_bash_autocomplete_file)

    if 'Not open source' == '{{ cookiecutter.open_source_license }}':
        remove_file('LICENSE')

    if '{{ cookiecutter.initialize_git_repository }}' == 'y':
        initialize_git_repository_if_necessary()

    if '{{ cookiecutter.initialize_venv_using_virtualenvwrapper }}' == 'y':
        initialize_venv_using_virtualenvwrapper()
