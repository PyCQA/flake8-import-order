flake8-import-order
===================

[![Build Status](https://travis-ci.org/public/flake8-import-order.png?branch=master)](https://travis-ci.org/public/flake8-import-order)

A flake8 plugin that checks the ordering of your imports matches the [Google
Style Guidelines](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html?showone=Imports_formatting#Imports_formatting).

i.e. That stdlib comes first, then 3rd party, then local packages, and that
each group is indivudually alphabetized.

It will not check anything else about the imports. Merely that they are grouped and ordered correctly.

Warnings
--------

This package adds 2 new flake8 warnings

* ``I100``: Your import statements are in the wrong order
* ``I101``: The names in your from import are in the wrong order.

Limitations
-----------

Currently these checks are limited to module scope imports only.
