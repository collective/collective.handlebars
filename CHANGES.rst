Changelog
=========


1.5 (unreleased)
----------------

- Python 3 / Plone 5.2 compatibility
  [adrianschulz, tomgross]

- Update dependencies
- Move to Github CI
- Apply black formatting
  [tomgross]


1.4.1 (2018-10-22)
------------------

- Add div-element to wrapper to support cases where only text is provided
  (otherwise plone.protect can fail)
  [tomgross]

1.4 (2018-09-10)
----------------

- Wrap tile so it works with newer versions of Mosaic
  [tomgross]


1.3 (2018-04-26)
----------------

- Set html/body parenthesis for tiles
  [tomgross]


1.2 (2016-10-31)
----------------

- Explicitly set UTF-8 encoding in response
  [tomgross]


1.1 (2016-10-28)
----------------

- Add support for helpers
  [tomgross]


1.0 (2016-10-28)
----------------

- Add persistent tile wrapper
  [tomgross]

- Unify names. It is now **HandlebarsTile**
  [tomgross]


1.0rc1 (2016-08-29)
-------------------

- Add registry for templates
  [tomgross]

- Fix i18n translate tests
  [tomgross]


1.0b1 (2016-07-25)
------------------

- Initial release.
  [tomgross]
