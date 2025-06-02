from setuptools import setup, find_namespace_packages

setup(
    name="mapped_tilings",
    version="0.1.0",
    description="A module for using mapped tilings.",
    author="Reed Acton, Christian Bean, and Abigail Ollson",
    author_email="c.n.bean@keele.ac.uk",
    packages=find_namespace_packages(),
    install_requires=[
        "comb_spec_searcher",
        "cayley_perms @ git+https://github.com/Ollson2921/CayleyPerms",
    ],  # external packages as dependencies
)
