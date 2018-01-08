"""setup.py: Packaging and distribution hub for project"""
from codecs import open
from os import path, listdir
import io

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
try:
    from setuphelpers import find_version, git_version
except ImportError:
    find_version = lambda x: '0.0.0'
    git_version = lambda: '0.0.0'

HERE = path.abspath(path.dirname(__file__))
__package_name__ = 'pyRobinhood'
__library_name__ = 'pyrobinhood'

def get_version(lib_path=__library_name__):
    """figure out __version__.py information

    Notes:
        https://github.com/ccpgames/setuphelpers#git_version

    Args:
        lib_path (str): path to library with __version__.py

    Returns:
        str: semantic version of package
    """
    ver_file = path.join(HERE, lib_path, '__version__.py')
    if path.isfile(ver_file):
        return find_version(ver_file)

    version = git_version()
    with io.open(ver_file, 'w', encoding='utf-8') as dunder_version:
        dunder_version.write('__version__ = \'{}\''.format(version))
    return version

class PyTest(TestCommand):
    """PyTest cmdclass hook for test-at-buildtime functionality

    Notes:
        http://doc.pytest.org/en/latest/goodpractices.html#manual-integration
    """
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = [
            'tests',
            '-rx',
            '-n',
            '4',
            '--cov=' + __library_name__,
            '--cov-report=term-missing',
            '--cov-config=.coveragerc'
        ]

    def run_tests(self):
        import shlex
        import pytest
        pytest_commands = []
        try:
            pytest_commands = shlex.split(self.pytest_args)
        except AttributeError:
            pytest_commands = self.pytest_args
        errno = pytest.main(pytest_commands)
        exit(errno)

class TravisTest(PyTest):
    """wrapper for Travis-CI run"""
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = [
            'tests',
            '-rx',
            '-m',
            'not auth',
            '-v',
            '--cov=' + __library_name__,
            '--cov-report=term-missing',
            '--cov-config=.coveragerc'
        ]

with open('README.rst', 'r', 'utf-8') as f:
    README = f.read()

setup(
    name=__package_name__,
    author='John Purcell',
    author_email='jpurcell.ee@gmail.com',
    url='https://github.com/lockefox/' + __package_name__,
    version=get_version(),
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='robinhood stocks trading REST API',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['LICENSE', 'README.rst', ]
    },
    setup_requires=["setuphelpers"],
    install_requires=[
        'requests',
        'six',
    ],
    tests_require=[
        'pytest',
        'pytest_cov',
        'pytest-xdist',
        'flaky',
        'jsonschema',
    ],
    extras_require={
        'dev':[
            'sphinx',
            'sphinxcontrib-napoleon',
        ]
    },
    cmdclass={
        'test':PyTest,
        'travis':TravisTest,
    },
)
