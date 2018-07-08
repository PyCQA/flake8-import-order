0.18 2018-07-08
---------------

* Add new Python 3.7 modules to the stdlib list, and support 3.7.

0.17.1 2018-03-05
-----------------

* Rebuild of 0.17 with the latest setuptools to fix an enum34
  dependency bug.

0.17 2018-02-11
---------------

* Add all Python3 modules to stdlib list (should be no more missing
  modules).
* Clarify the error messages (more context).
* Allow styles to override specific checks.
* Correct the edited style to match the actual edited style guide.
* Add pycharm style, to match the pycharm auto formatter.


0.16 2017-11-26
---------------

* Change spacing determination to consider only blank newlines as a
  space. This adds NewLine nodes to the checker and hence could break
  custom styles (that use the nodes directly). This also drops the
  asttokens dependency as it is no longer required.
* Understand the existance of namespaced packages, thereby allowing
  different namespaced pacakages to be defined as local or third party.

0.15 2017-11-06
---------------

* Drop Python 3.3 support, as Python 3.3 is beyond it's end of lfe.
* Correct the flake8 entrypoint to report all ``I`` errors, this may
  result in ``I2XX`` errors being reported that were absent
  previously.
* Support in-line ``# noqa`` comments specifing only the error codes
  to be ignored, e.g., ``# noqa: I101``.
* Accept only ``# noqa`` directives on the line reporting the error,
  see limitations.


0.14.3 2017-11-01
-----------------

* Bug fix, allow for noqa directives to work with I202.

0.14.2 2017-10-30
-----------------

* Bug fix, ensure the plugin is invoked by flake8.

0.14.1 2017-10-27
-----------------

* Bug fix, cope with multi-line imports when considering I202.

0.14 2017-10-24
---------------

* Fixed I201 error raising for cryptography style.
* Added I202 error when there is an additional newline in a section of
  imports.
* Added ``ntpath`` and ``os2emxpath`` to stdlib list.

0.13 2017-07-29
---------------

* Added ``secrets`` to stdlib list.
* Allow for any style to use application-package grouping.

0.12 2017-02-11
---------------

* Added new Edited style, this is equivalent to the Smarkets style
  except that values specified in the ``application-package-names``
  option must be imported after third-party import statements
* Added ability to extend a style using an entrypoint.
* Fix ambiguous I100 error, now lists correct packages.

0.11 2016-11-09
---------------

* Enforce lexicographic ordering for Google, Smarkets and AppNexus
  styles. This may introduce warnings not present in previous
  releases relating to case sensitivity.
* Fix I100 case sensitivity for ungrouped imports, again enforcing
  lexicographic ordering.

0.10 2016-10-16
---------------

* Added new AppNexus style, this is equivalent to the google style
  except that values specified in the `application-package-names`
  option must be imported after third-party import statements
* Fixed ungrouped ordering bug whereby I100 wasn't triggered.

0.9.2 2016-08-05
----------------

* Fix error when checking from stdin using flake8 3.0.

0.9.1 2016-07-27
----------------

* Fix case sensitivity bug for Google and Smarkets style.

0.9 2016-07-26
--------------

* Drop pep8 requirement and replace with pycodestyle.
* Support Flake8 3.0 (alongside Flake8 2.X).
* Drop Python2.6 compatibility.
* Fixed a bug where intermixed 1st and 3rd party imports cause an
  error with the PEP8 style.
* Fixed a bug whereby the I101 recommended ordering wasn't a valid
  ordering in the cryptography style.

0.8
---

* Added profile, cProfile, pstats and typing to stdlib list.
* Added new PEP8 style, that enforces grouping of importes but allows
  any ordering within the groups.

0.7
---

* Added new Smarkets style, this is equivalent to the google style
  except that any `import X` statements must come before any `from X
  import y` statments.

0.6.2
-----

* Fixed a bug where I101 messages were not suggesting the correct order in the
  default style.  The output message now outputs a message that matches the
  selected style.

0.6.1
-----

* Fixed a bug where I101 messages were not suggesting the correct order.
* Extended test harness to be able to check error messages as well as codes.
