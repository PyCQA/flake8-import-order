flake8-import-order
===================

A flake8 plugin that checks the ordering of your imports matches the Google
Style Guidelines.

i.e. That stdlib comes first, then 3rd party, then local packages, and that
each group is indivudually alphabetized.

Warnings
--------

This package adds 2 new flake8 warnings

* ``I100``: Your import statements are in the wrong order
* ``I101``: The names in your from import are in the wrong order.

Limitations
-----------

Currently these checks are limited to module scope imports only and there are
some known issues around imports that use ``as`` to rename symbols.
