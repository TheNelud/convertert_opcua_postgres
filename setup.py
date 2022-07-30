import os
from setuptools import setup
from nvpy import nvpy

setup(
    name="converter",
    version="1.0",
    author="by TheNelud",
    author_email="rpvdev@vk.com",
    description="Coтverter for opcua in postgres ",
    license="BSD",
    packages=['converter'],
    entry_points={
        'console_scripts': ['converter = converter.converter:main']
    },
    data_files=[
        ('share/applications/', ['vxlabs-myscript.desktop'])
    ],
    classifiers=[
        "License :: OSI Approved :: BSD License",
    ],
)
