flake8-import-order
===================

|Build Status|

A `flake8 <http://flake8.readthedocs.org/en/latest/>`__ and
`Pylama <https://github.com/klen/pylama>`__ plugin that checks the
ordering of your imports.

In general stdlib comes first, then 3rd party, then local packages, and
that each group is individually alphabetized, see Configuration section
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

You will want to set the ``application-import-names`` option to a
comma separated list of names that should be considered local to your
application. These will be used to help categorise your import
statements into the correct groups. Note that relative imports are
always considered local.

You will want to set the ``application-package-names`` option to a
comma separated list of names that should be considered local to your
company or organisation, but which are obtained using some sort of
package manager like Pip, Apt, or Yum.  Typically, code representing the
values listed in this option is located in a different repository than
the code being developed.  This option is only supported if using the
``appnexus`` style.

``import-order-style`` controls what style the plugin follows
(``cryptography`` is the default):

* ``cryptography`` - see an `example <https://github.com/PyCQA/flake8-import-order/blob/master/tests/test_cases/complete.py>`__
* ``google`` - style described in `Google Style Guidelines <https://google.github.io/styleguide/pyguide.html?showone=Imports_formatting#Imports_formatting>`__, see an `example <https://github.com/PyCQA/flake8-import-order/blob/master/tests/test_cases/complete_google.py>`__
* ``smarkets`` - style as ``google`` only with `import` statements before `from X import ...` statements, see an `example <https://github.com/PyCQA/flake8-import-order/blob/master/tests/test_cases/complete_smarkets.py>`__
* ``appnexus`` - style as ``google`` only with `import` statements for packages local to your company or organisation coming after `import` statements for third-party packages, see an `example <https://github.com/PyCQA/flake8-import-order/blob/master/tests/test_cases/complete_appnexus.py>`__
* ``pep8`` - style that only enforces groups without enforcing the order within the groups

Limitations
-----------

Currently these checks are limited to module scope imports only.
Conditional imports in module scope will also be ignored.

Classification of an imported module is achieved by checking the
module against a stdlib list and then if there is no match against the
``application-import-names`` list. (If using the ``appnexus`` style, also
the ``application-package-names`` list.) Only if none of these lists
contain the imported module will it be classified as third party.

``I201`` only checks that groups of imports are not consecutive and only
takes into account the first line of each import statement. This means
that multi-line from imports, comments between imports and so on may
cause this error not to be raised correctly in all situations. This
restriction is due to the data provided by the stdlib ``ast`` module.

Imported modules are classified as stdlib if the module is in a
vendored list of stdlib modules. This list is based on the latest
release of Python and hence the results can be misleading. This list
is also the same for all Python versions because otherwise it would
be impossible to write programs that work under both Python 2 and 3
*and* pass the import order check.

.. |Build Status| image:: https://travis-ci.org/PyCQA/flake8-import-order.png?branch=master
   :target: https://travis-ci.org/PyCQA/flake8-import-order
