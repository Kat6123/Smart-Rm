# -*- coding: utf-8 -*-
import os.path
import setuptools


setuptools.setup(
    name='simple_rm',
    packages=setuptools.find_packages(),
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README.rst')
    ).read(),
    include_package_data=True,
    test_suite="test",
    entry_points={
        'console_scripts': [
            'smart_rm = simple_rm.main_remove:main'
            # 'trash = smart_rm.trash_main:main'
            ]
    }
)
