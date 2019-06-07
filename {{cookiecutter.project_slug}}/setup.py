from pathlib import Path
from setuptools import find_packages, setup

readme = Path('README.rst').read_text(encoding="utf-8")
history = Path('docs/history.rst').read_text(encoding="utf-8")

runtime_requirements = [{% if cookiecutter.command_line_interface | lower == 'click' %}
    'click>=7.0',
{% endif %}]
development_requirements = [
    'pip>=19.0.2',
    'bumpversion>=0.5.3',
    'wheel>=0.32.3',
    'watchdog>=0.9.0',
    'flake8>=3.6.0',
    'tox>=3.6.1',
    'coverage>=4.5.2',
    'Sphinx>=1.8.3',
    'twine>=1.12.1',
    'pluggy>=0.7.0',
    'mypy>=0.650',{% if cookiecutter.use_pytest == 'y' %}
    'pytest>=3.8.2',
    'pytest-runner>=4.2',
    'pytest-mock>=1.10.1',{% endif %}
]

{%- set license_classifiers = {
    'MIT license': 'License :: OSI Approved :: MIT License',
    'BSD license': 'License :: OSI Approved :: BSD License',
    'ISC license': 'License :: OSI Approved :: ISC License (ISCL)',
    'Apache Software License 2.0': 'License :: OSI Approved :: Apache Software License',
    'GNU General Public License v3': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
} %}

setup(
    author="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
    author_email="{{ cookiecutter.email.replace('\"', '\\\"') }}",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
{%- if cookiecutter.open_source_license in license_classifiers %}
        '{{ license_classifiers[cookiecutter.open_source_license] }}',
{%- endif %}
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="{{ cookiecutter.project_short_description }}",
    {%- if cookiecutter.command_line_interface|lower == 'click' %}
    entry_points={
        'console_scripts': [
            '{{ cookiecutter.project_slug }}={{ cookiecutter.project_slug }}.cli:main',
        ],
    },
    {%- endif %}
    install_requires=runtime_requirements,
    extras_require={
        'dev': development_requirements
    },
{%- if cookiecutter.open_source_license in license_classifiers %}
    license="{{ cookiecutter.open_source_license }}",
{%- endif %}
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='{{ cookiecutter.project_slug }}',
    name='{{ cookiecutter.project_slug }}',
    packages=find_packages(include=['{{ cookiecutter.project_slug }}', '{{ cookiecutter.project_slug }}.*']),
    setup_requires=development_requirements,
    test_suite='tests',
    tests_require=development_requirements,
    url='https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}',
    version='{{ cookiecutter.version }}',
    zip_safe=False,
)
