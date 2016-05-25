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
