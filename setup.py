#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
https://github.com/kennethreitz/setup.py

Note: To use the 'upload' functionality of this file, you must:
  $ pip install twine
"""
from __future__ import print_function
import io
import sys
from os import path, system
from shutil import rmtree

# Always prefer setuptools over distutils
from setuptools import find_packages, setup, Command

here = path.abspath(path.dirname(__file__))

# Import the README.rst and use it as the long-description.
with io.open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


class PublishCommand(Command):
    """Support setup.py publish."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        system('twine upload dist/*')

        sys.exit()


# Where the magic happens:
setup(
    name='pizzapi',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.0.6',

    description='A Python wrapper for the Dominos Pizza API',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/aluttik/pizzapi',

    # Author details
    author='aluttik',
    author_email='aluttik@gmail.com',

    # What does your project relate to?
    keywords='dominos pizza api',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # TODO: Add testing/support for more python versions
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    # TODO: Add a command line tool
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    #     'console_scripts': [
    #         'pizzapi=pizzapi:main'
    #     ],
    # },

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'pyhamcrest',
        'requests', 
        'xmltodict',
    ],
    include_package_data=True,
    tests_require=[
        'mock',
        'pytest',
    ],
    setup_requires=["pytest-runner"],

    # setup.py publish support.
    cmdclass={
        'publish': PublishCommand,
    },
)
