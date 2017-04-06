import sys
from setuptools import setup, find_packages

install_requires = [
    'python-neutronclient>=6.1.0',
    'six',
    'prettytable',
    'termcolor'
]
test_requires = []

setup(
    name='os-cleanup',
    version='0.1',
    description="Cleanup Routine for Openstack Project resources",
    author="S.Suresh Kumar",
    author_email="sureshkumarr.s@gmail.com",
    url="https://github.com/sureshkvl/os-cleanup",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    scripts=[],
    license="Apache",
    entry_points={
    },
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4'
    ]
)
