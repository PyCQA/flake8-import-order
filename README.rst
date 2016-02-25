flake8-import-order
===================

|Build Status|

A `flake8 <http://flake8.readthedocs.org/en/latest/>`__ and
`Pylama <https://github.com/klen/pylama>`__ plugin that checks the
ordering of your imports.

In general stdlib comes first, then 3rd party, then local packages, and
that each group is indivudually alphabetized, see Configuration section
for details.

It will not check anything else about the imports. Merely that they are
grouped and ordered correctly.

This plugin is under somewhat active development and is heavily
influenced by the personal preferences of the developers of
`cryptography <https://github.com/pyca/cryptography>`__. Expect
seemingly random changes and configuration changes as we figure out how
it should work.

Warnings
--------

This package adds 3 new flake8 warnings

-  ``I100``: Your import statements are in the wrong order.
-  ``I101``: The names in your from import are in the wrong order.
-  ``I201``: Missing newline between sections or imports.

Configuration
-------------

You will want to set the ``application-import-names`` option to a comma
separated list of names that should be considered local to your
application. These will be used to help categorise your import
statements into the correct groups.

``import-order-style`` controls what style the plugin follows
(``cryptography`` is the default):

* ``cryptography`` - see an `example <https://github.com/public/flake8-import-order/blob/master/tests/test_cases/complete.py>`__
* ``google`` - style described in `Google Style Guidelines <http://google-styleguide.googlecode.com/svn/trunk/pyguide.html?showone=Imports_formatting#Imports_formatting>`__, see an `example <https://github.com/public/flake8-import-order/blob/master/tests/test_cases/complete_google.py>`__
* ``smarkets`` - style as ``google`` only with `import` statements before `from X import ...` statements, see an `example <https://github.com/public/flake8-import-order/blob/master/tests/test_cases/complete_smarkets.py>`__

Limitations
-----------

Currently these checks are limited to module scope imports only.
Conditional imports in module scope will also be ignored. The
classification of an import as being non-stdlib of some kind depends on
that package actually being installed.

``I103`` only checks that groups of imports are not consecutive and only
takes into account the first line of each import statement. This means
that multi-line from imports, comments between imports and so on may
cause this error not to be raised correctly in all situations. This
restriction is due to the data provided by the stdlib ``ast`` module.

.. |Build Status| image:: https://travis-ci.org/public/flake8-import-order.png?branch=master
   :target: https://travis-ci.org/public/flake8-import-order
