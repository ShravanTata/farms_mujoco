#!/usr/bin/env python
""" Setup script """

from setuptools import setup

setup(
    name="salamander_results",
    version="0.1",
    author="Jonathan Arreguit",
    author_email="jonathan.arreguitoneill@epfl.ch",
    description="Salamander results viewer and analysis",
    # license="BSD",
    keywords="salamander results analysis",
    # url="",
    packages=['salamander_results'],
    scripts=[
        "scripts/salamander_plot_positions.py",
        "scripts/salamander_plot_all_positions.py"
    ]
    # long_description=read('README'),
    # classifiers=[
    #     "Development Status :: 3 - Alpha",
    #     "Topic :: Utilities",
    #     "License :: OSI Approved :: BSD License",
    # ],
    # package_data={'salamander_messages': [
    #     'salamander_generation/templates/*',
    #     'salamander_generation/config/*'
    # ]},
    # include_package_data=True
)
