.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
Handlebars.js templating for Plone
==============================================================================

The idea of this package is to provide handlebars.js support for Plone.
It is a developer addon and provides additional variants of
BrowserView, Portlet, Viewlet and Tile which utilizes handlbars.js_
templating instead of TAL. It can be used to optimze the workflow
between designers and Plone developers.

The product was developed and tested with Plone 5 but might work
with older versions too.


Features
--------

Provides the following view components with handlebars support:

 - BrowserView
 - Plone template
 - Tile

Examples
--------

This add-on can be seen in action at the following sites:
- Is there a page on the internet where everybody can see the features?


Documentation
-------------

Full documentation for end users can be found in the "docs" folder, and is also available online at http://docs.plone.org/foo/bar

Installation
------------

Install collective.handlebars by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.handlebars


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.handlebars/issues
- Source Code: https://github.com/collective/collective.handlebars
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@example.com


License
-------

The project is licensed under the GPLv2.

.. _handlebars.js: http://handlebarsjs.com/
