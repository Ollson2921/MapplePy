###############################
MapplePy
###############################

MapplePy is a python library for enumerating Cayley permutation classes which avoid non-classical patterns and grid classes.

A Cayley permutation is a word `π ∈ ℕ*` such that every number between 1 and the maximum value of `π` appears at least once. Cayley permutations can be seen as a generalisation of permutations where repeated values are allowed. Definitions of pattern containment and Cayley permutation classes follow the same ideas as defined for permutations where the patterns contained are also Cayley permutations, so the Cayley permutation class Av(11) describes all permutations. Cayley permutations are in bijection with ordered set partitions.

If you need support, you can join us in our `Discord support server`_.

.. _Discord support server: https://discord.gg/ngPZVT5

==========
Installing
==========

To install MapplePy on your system, run the following after cloning the repository:

.. code-block:: bash

    ./pip install .

It is also possible to install MapplePy in development mode to work on the
source code, in which case you run the following after cloning the repository:

.. code-block:: bash

    ./pip install -e .
    
