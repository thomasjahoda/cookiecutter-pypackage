"""
Script to execute after creating the project.
- Encrypts the PyPi password to the .travis.yml
- Sets the test runner to pytest if using PyCharm
"""

import configparser
import subprocess
from pathlib import Path
from typing import Tuple, cast
import xml.etree.ElementTree as ElementTree

try:
    import yaml
except ImportError as error:
    print("Attempting to install pyyaml")
    subprocess.run(["pip", "install", "pyyaml"])
    try:
        import yaml
    except ImportError as error:
        raise Exception(
            "Could not install pyyaml automatically successfully, please install it manually first") from error

TRAVIS_YML_FILE = Path("../.travis.yml").expanduser()
TRAVIS_YML_ENCRYPTED_PASSWORD_PLACEHOLDER_VALUE = "PLEASE_REPLACE_ME"


def encrypt_pypi_password_for_travis_if_necessary():
    travis_yml_content = yaml.safe_load(TRAVIS_YML_FILE.read_text(encoding="utf-8"))
    project_owner_pypi_username = travis_yml_content["deploy"]["user"]
    project_owner_pypi_encrypted_password = travis_yml_content["deploy"]["password"]["secure"]
    if project_owner_pypi_encrypted_password == TRAVIS_YML_ENCRYPTED_PASSWORD_PLACEHOLDER_VALUE:
        _encrypt_pypi_password_for_travis(project_owner_pypi_username)
    else:
        print(f"Travis password has already been encrypted in {TRAVIS_YML_FILE.name}.")


def _encrypt_pypi_password_for_travis(project_owner_pypi_username: str):
    pypi_username, pypi_password = _get_pypi_credentials()
    if project_owner_pypi_username != project_owner_pypi_username:
        raise Exception(f"The pypi username stated in {TRAVIS_YML_FILE.name} ({project_owner_pypi_username}) "
                        f"does not match the one configured in the current environments "
                        f"pypi settings ({pypi_username}). "
                        f"Please check your ~/.pypirc file or your keyring properties for pypi.")
    try:
        result = subprocess.run(
            ["travis", "encrypt", "--skip-version-check", "--skip-completion-check", "--no-interactive"],
            input=bytes(pypi_password, encoding="utf-8"),
            capture_output=True,
        )
    except FileNotFoundError as exception:
        raise Exception("Command 'travis' needs to be available on path. "
                        "Please install https://github.com/travis-ci/travis.rb#installation") from exception
    result.check_returncode()
    output = str(result.stdout, encoding="utf-8")
    encrypted_password = output[1:-2]

    travis_yml_text = TRAVIS_YML_FILE.read_text(encoding="utf-8")
    travis_yml_text = travis_yml_text.replace(TRAVIS_YML_ENCRYPTED_PASSWORD_PLACEHOLDER_VALUE, encrypted_password)
    TRAVIS_YML_FILE.write_text(travis_yml_text, encoding="utf-8")
    print(f"Updated {TRAVIS_YML_FILE.name} with encrypted pypi password. Please commit it in Git.")


def _get_pypi_credentials() -> Tuple[str, str]:
    pypirc_file = Path("~/.pypirc").expanduser()
    if pypirc_file.is_file():

        config = configparser.ConfigParser()
        config.read(pypirc_file)
        pypi_username = config['pypi']['username']
        pypi_password = config['pypi']['password']
        print(f"Using pypi credentials found in {pypirc_file}")
        return pypi_username, pypi_password
    else:
        # TODO check keyring if pypi credentials are there in case ~/.pypirc does not exist.
        #  https://twine.readthedocs.io/en/latest/#id6
        raise Exception("Please create the file ~/.pypirc with your pypi user credentials as documented at "
                        "https://packaging.python.org/guides/distributing-packages-using-setuptools/#id78\n"
                        "Support for the Keyring credentials as documented at "
                        "https://twine.readthedocs.io/en/latest/#id6 is currently unsupported but contributing "
                        "is wished.")


encrypt_pypi_password_for_travis_if_necessary()


def set_pycharm_test_runner_to_pytest():
    project_name = cast(Path, Path.cwd()).parent.name
    idea_project_config_file = Path("../.idea", f"{project_name}.iml")
    if idea_project_config_file.exists():
        tree = ElementTree.parse(idea_project_config_file)
        root = tree.getroot()
        test_runner_element: ElementTree = next((element for element in root.findall("component")
                                                 if element.get("name") == "TestRunnerService"), None)
        updated = False
        if test_runner_element is not None:
            project_test_runner_element = next((element for element in test_runner_element.findall("option")
                                                if element.get("name") == "PROJECT_TEST_RUNNER"), None)
            if project_test_runner_element is not None:
                if project_test_runner_element.get("value") != "pytest":
                    project_test_runner_element.set("value", "pytest")
                    updated = True
            else:
                _create_project_test_runner_element(test_runner_element)
                updated = True

            project_configuration_element = next((element for element in test_runner_element.findall("option")
                                                  if element.get("name") == "projectConfiguration"), None)
            if project_configuration_element is not None:
                if project_configuration_element.get("value") != "pytest":
                    project_configuration_element.set("value", "pytest")
                    updated = True
            else:
                _create_project_configuration_element(test_runner_element)
                updated = True
        else:
            test_runner_service = ElementTree.SubElement(root, "component",
                                                         {"name": "TestRunnerService"})
            _create_project_configuration_element(test_runner_service)
            _create_project_test_runner_element(test_runner_service)
            updated = True

        if updated:
            tree.write(idea_project_config_file, encoding="UTF-8", xml_declaration=True)
            print(f"Updated test runner in {idea_project_config_file} to pytest")
        else:
            print(f"Test runner in {idea_project_config_file} was already pytest")


def _create_project_configuration_element(parent):
    ElementTree.SubElement(parent, "option",
                           {"name": "projectConfiguration", "value": "pytest"})


def _create_project_test_runner_element(parent):
    return ElementTree.SubElement(parent, "option",
                                  {"name": "PROJECT_TEST_RUNNER", "value": "pytest"})


set_pycharm_test_runner_to_pytest()
