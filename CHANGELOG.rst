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
