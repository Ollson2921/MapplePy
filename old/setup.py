from setuptools import setup

setup(
    name="mapplings",
    version="1.0",
    description="A module for using mapplings.",
    author="Reid Acton, Christian Bean, and Abigail Ollson",
    author_email="c.n.bean@keele.ac.uk",
    packages=[
        "mapplings",
    ],
    install_requires=[
        "comb_spec_searcher"
        #   "cayley_perms" # need to install this manually right now
    ],  # external packages as dependencies
)
