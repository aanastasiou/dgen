"""Athanasios Anastasiou April 2017
A simple setup file to install DGen"""

import os
from setuptools import setup

def read(fname):
    """Reads a text file and returns its content
    
    Utility function to read the long description stored in the README.md
    
    Args:
        fname: A string representing the filename to read from a disk
        
    Returns:
        A string representing the content of the file.
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "DGen",
    version = "0.0.1",
    author = "Athanasios Anastasiou",
    author_email = "athanastasiou@gmail.com",
    description = ("An object oriented approach to synthetic clinical data generation"),
    license = "GPL",
    keywords = "synthetic data clinical framework",
    url = "http://myurl.com",
    packages=['DGen', "DGen.epi", "examples"],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Database",
        "Topic :: Games/Entertainment :: Simulation",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
    install_requires=[
        "rstr",
        "bunch",
    ]
)
