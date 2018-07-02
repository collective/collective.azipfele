Changelog
=========

2.0.2 (2018-07-02)
------------------

- Fix #2: ZipIt Error handling canonot handle missing context
  [do3cc, jensens]

2.0.1 (2017-10-27)
------------------

- Allow anonymous initiation of taskqueue processing
  [agitator]


2.0.0 (2017-01-12)
------------------

  Add ``collective.taskqueue`` implementation.
  [jensens]

- Refactor queuing code in order to allow additionla queue implementations.
  This is a breaking change! All custom code importing from old ``taskzamqp.py`` needs adjustments.
  The existing code and additional code goes under ``queue`` subdirectory.
  [jensens]

- isort headers according to Plone rules.
  [jensens]


1.1.2 (2014-12-19)
------------------

- "apostroph no catastroph", unicode strings for logging
  [agitator]


1.1.1 (2014-10-05)
------------------

- fix: bug in download view
  [jensens]


1.1 (2014-09-16)
----------------

- removed superfluos dependency on collective.js.angular
  [jensens]


1.0
---

- make it work
