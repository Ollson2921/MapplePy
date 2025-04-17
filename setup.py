from setuptools import setup

setup(
    name="mapped_tilings",
    version="1.0",
    description="A module for using mapped tilings.",
    author="Reid Acton, Christian Bean, and Abigail Ollson",
    author_email="c.n.bean@keele.ac.uk",
    packages=["mapplings"],
    install_requires=["comb_spec_searcher"],  # external packages as dependencies
)
