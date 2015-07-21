#!/usr/bin/env python3

from distutils.core import setup

setup(
    name="splash",
    version="v0.0.0",
    description="Speedreading software",
    long_description="A program that allows you to read texts really fast",
    author="Jonas Jelten (see COPYING for contributors)",
    author_email="jj@sft.mx",
    url="https://github.com/SFTtech/splash",
    license="GPLv3+",
    packages=["splash"],
    scripts=["bin/splash"],
    classifiers=[
        ("License :: OSI Approved :: GNU General Public License v3 "
         "or later (GPLv3+)"),
        "Operating System :: OS Independent",
    ],
)
