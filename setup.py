from setuptools import setup, find_packages
from os.path import join, dirname
from smart_rm import __version__

setup(
    name='smart_rm',
    version=__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    include_package_data=True,
    test_suite="test",
    install_requires=['argparse'],
    entry_points={
        'console_scripts': ['smart_rm = smart_rm.main:main']}
)
