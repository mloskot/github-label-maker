from setuptools import setup

setup(
    name="gh_label_maker",
    version="0.0.1",
    description="CLI tool for managing github labels",
    packages=["gh_label_maker"],
    install_requires=["PyGithub==1.56"],
    classifiers=["Programing Language :: Python :: 3.10"]
)
