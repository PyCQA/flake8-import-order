flake8-import-order
===================

|Build Status|

A `flake8 <http://flake8.readthedocs.org/en/latest/>`__ and `Pylama
<https://github.com/klen/pylama>`__ plugin that checks the ordering of
your imports. It does not check anything else about the
imports. Merely that they are grouped and ordered correctly.

In general stdlib comes first, then 3rd party, then local packages,
and that each group is individually alphabetized, however this depends
on the style used. Flake8-Import-Order supports a number of `styles
<#styles>`_ and is extensible allowing for `custom styles
<#extending-styles>`_.

This plugin was originally developed to match the style preferences of
the `cryptography <https://github.com/pyca/cryptography>`__ project,
with this style remaining the default.

Warnings
--------

This package adds 4 new flake8 warnings

-  ``I100``: Your import statements are in the wrong order.
-  ``I101``: The names in your from import are in the wrong order.
-  ``I201``: Missing newline between import groups.
-  ``I202``: Additional newline in a group of imports.

Styles
------

The following styles are directly supported,

* ``cryptography`` - see an `example <https://github.com/PyCQA/flake8-import-order/blob/master/tests/test_cases/complete_cryptography.py>`__
* ``google`` - style described in `Google Style Guidelines <https://google.github.io/styleguide/pyguide.html?showone=Imports_formatting#313-imports-formatting>`__, see an `example <https://github.com/PyCQA/flake8-import-order/blob/master/tests/test_cases/complete_google.py>`__
* ``smarkets`` - style as ``google`` only with `import` statements before `from X import ...` statements, see an `example <https://github.com/PyCQA/flake8-import-order/blob/master/tests/test_cases/complete_smarkets.py>`__
* ``appnexus`` - style as ``google`` only with `import` statements for packages local to your company or organisation coming after `import` statements for third-party packages, see an `example <https://github.com/PyCQA/flake8-import-order/blob/master/tests/test_cases/complete_appnexus.py>`__
* ``edited`` - see an `example <https://github.com/PyCQA/flake8-import-order/blob/master/tests/test_cases/complete_edited.py>`__
* ``pycharm`` - style as ``smarkets`` only with case sensitive sorting imported names
* ``pep8`` - style that only enforces groups without enforcing the order within the groups

You can also `add your own style <#extending-styles>`_ by extending ``Style``
class.

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
package manager like Pip, Apt, or Yum.  Typically, code representing
the values listed in this option is located in a different repository
than the code being developed.  This option is only accepted in the
supported ``appnexus`` or ``edited`` styles or in any style that
accepts application package names.

The ``application-import-names`` and ``application-package-names`` can
contain namespaced packages or even exact nested module names. (This
is possible with 0.16 onwards).

``import-order-style`` controls what style the plugin follows
(``cryptography`` is the default).

Limitations
-----------

Currently these checks are limited to module scope imports only.
Conditional imports in module scope will be ignored except imports
under ```if TYPE_CHECKING:``` block.

Classification of an imported module is achieved by checking the
module against a stdlib list and then if there is no match against the
``application-import-names`` list and ``application-package-names`` if
the style accepts application-package names. Only if none of these
lists contain the imported module will it be classified as third
party.

These checks only consider an import against its previous import,
rather than considering all the imports together. This means that
``I100`` errors are only raised for the latter of adjacent imports out
of order. For example,

.. code-block:: python

    import X.B
    import X  # I100
    import X.A

only ``import X`` raises an ``I100`` error, yet ``import X.A`` is also
out of order compared with the ``import X.B``.

Imported modules are classified as stdlib if the module is in a
vendored list of stdlib modules. This list is based on the latest
release of Python and hence the results can be misleading. This list
is also the same for all Python versions because otherwise it would
be impossible to write programs that work under both Python 2 and 3
*and* pass the import order check.

The ``I202`` check will consider any blank line between imports to
count, even if the line is not contextually related to the
imports. For example,

.. code-block:: python

    import logging
    try:
        from logging import NullHandler
    except ImportError:
        class NullHandler(logging.Handler):
            """Shim for version of Python < 2.7."""

            def emit(self, record):
                pass
    import sys  # I202 due to the blank line before the 'def emit'

will trigger a ``I202`` error despite the blank line not being
contextually related.

Extending styles
----------------

You can add your own style by extending ``flake8_import_order.styles.Style``
class. Here's an example:

.. code-block:: python

    from flake8_import_order.styles import Cryptography


    class ReversedCryptography(Cryptography):
        # Note that Cryptography is a subclass of Style.

        @staticmethod
        def sorted_names(names):
            return reversed(Cryptography.sorted_names(names))

By default there are five import groupings or sections; future,
stdlib, third party, application, and relative imports. A style can
choose to accept another grouping, application-package, by setting the
``Style`` class variable ``accepts_application_package_names`` to
True, e.g.

.. code-block:: python

    class PackageNameCryptography(Cryptography):
        accepts_application_package_names = True

To make flake8-import-order able to discover your extended style, you need to
register it as ``flake8_import_order.styles`` using setuptools' `entry points
<https://setuptools.readthedocs.io/en/latest/pkg_resources.html#entry-points>`__
mechanism:

.. code-block:: python

    # setup.py of your style package
    setup(
        name='flake8-import-order-reversed-cryptography',
        ...,
        entry_points={
            'flake8_import_order.styles': [
                'reversed = reversedcryptography:ReversedCryptography',
                # 'reversed' is a style name.  You can pass it to
                # --import-order-style option
                # 'reversedcryptography:ReversedCryptography' is an import path
                # of your extended style class.
            ]
        }
    )

.. |Build Status| image:: https://travis-ci.org/PyCQA/flake8-import-order.svg?branch=master
   :target: https://travis-ci.org/PyCQA/flake8-import-order
