# !/usr/bin/env python
from distutils.core import setup

runtime_requirements = []
development_requirements = [
    'pytest==5.4.3',
    'tox==3.20.1',
    'cookiecutter>=1.7.2',
    'pytest-cookies==0.5.1',
    'watchdog==0.10.3',
    'alabaster==0.7.12',
    'PyYAML==5.3.1',
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
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
    ],
    install_requires=runtime_requirements,
    extras_require={
        'dev': development_requirements
    },
)
