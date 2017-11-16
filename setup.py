"""
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import find_packages, setup

setup(
    name='pizzapi',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.0.3',

    description='A Python wrapper for the Dominos Pizza API',

    # The project's main homepage.
    url='https://github.com/wardcraigj/pizzapi',

    # Author details
    author='wardcraigj forked from aluttik',
    author_email='ward.craig.j@gmail.com',

    # What does your project relate to?
    keywords='dominos pizza api',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['tests']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['requests', 'xmltodict'],
    extras_require={
        'test': ['mock', 'PyHamcrest', 'pytest'],
    },
)