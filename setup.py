# !/usr/bin/env python
from distutils.core import setup

runtime_requirements = []
development_requirements = [
    'pytest==3.4.2',
    'tox==2.9.1',
    'cookiecutter>=1.4.0',
    'pytest-cookies==0.3.0',
    'watchdog==0.8.3',
    'alabaster==0.7.10',
    'pip-tools',
    'cookiecutter',
]

setup(
    name='cookiecutter-pypackage',
    packages=[],
    version='0.1.0',
    description='Cookiecutter template for a Python 3 package with strict type checking and linter settings',
    author='Thomas Jahoda',
    license='BSD',
    author_email='thomasjahoda@users.noreply.github.com',
    url='https://github.com/thomasjahoda/cookiecutter-pypackage',
    keywords=['cookiecutter', 'template', 'package', ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
    ],
    install_requires=runtime_requirements,
    extras_require={
        'dev': development_requirements
    },
)
