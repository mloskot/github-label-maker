from setuptools import setup

setup(
    name="gh_label_maker",
    version="0.0.1",
    description="CLI tool for managing github labels",
    packages=["gh_label_maker"],
    install_requires=["PyGithub==1.56"],
    entry_points={
        "console_scripts": ['gh_label_maker=gh_label_maker.cli:run']
    },
    classifiers=["Programming Language :: Python :: 3.10"]
)
