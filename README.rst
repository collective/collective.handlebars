.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
Handlebars.js templating for Plone
==============================================================================

.. image:: https://travis-ci.org/collective/collective.handlebars.svg?branch=master
       :target: https://travis-ci.org/collective/collective.handlebars

The idea of this package is to provide handlebars.js support for Plone.
It is a developer addon and provides additional variants of
BrowserView, Portlet, Viewlet and Tile which utilizes `handlebars.js <http://handlebarsjs.com/>`_
templating instead of TAL. It can be used to optimze the workflow
between designers and Plone developers.

The product was developed and tested with Plone 5 but might work
with older versions too.

This product does not do anything user related on itself!
It can not be installed as a Plone addon. What it does is to provide an API
for developers to integrate an alternative templating engine into Plone.

Features
--------

The prodcut provides the following view components with handlebars support:

 - BrowserView
 - Plone template
 - Tile

Since portlets and viewlets do not make any assumtion on the
templating and return everything which is returned by the
render-method of the Renderer they are supported too.

Examples
--------

A handlebar BrowserView: ::

  from collective.handlebars.browser.views import HandlebarsBrowserView

  class HBSBrowserView(HandlebarsBrowserView):

      def get_contents(self):
          return {'msg': u'Hello World!'}

And the according configure.zcml: ::

  <configure
      xmlns="http://namespaces.zope.org/zope"
      xmlns:browser="http://namespaces.zope.org/browser"
      i18n_domain="mydomain">

    <browser:page
         name="carousel_view"
         for="*"
         class=".views.HBSBrowserView"
         template="helloworld.hbs"
         permission="zope2.View"
         />


A handlebar Plone template: ::

  from collective.handlebars.browser.views import HandlebarsPloneView

  class CarouselView(HandlebarsPloneView):

      def get_contents(self):
          images = self.context.listFolderContents(
              contentFilter={'portal_type': ['Image', ]})

           slides = [{'title': safe_unicode(img.Title()),
                      'category': safe_unicode(img.Description()),
                      'link': img.remoteUrl,
                      'image': scale(img)} for img in images]

           return {'slides': slides, }}

And the according configure.zcml: ::

  <configure
      xmlns="http://namespaces.zope.org/zope"
      xmlns:browser="http://namespaces.zope.org/browser"
      i18n_domain="mydomain">

    <browser:page
         name="carousel_view"
         for="*"
         class=".views.CarouselView"
         template="carousel.hbs"
         permission="zope2.View"
         />

  </configure>

A handlebar portlet: ::

  from collective.handlebars.browser.views import HandlebarsMixin
  from plone.app.multilingual.browser.selector import LanguageSelectorViewlet

  class LanguageSwitcherRenderer(base.Renderer, HandlebarsMixin):
      """ Render a language switcher portlet
      """

      def get_contents(self):
          """ Get available and current site language
          :return: dictonary ()
          """
          viewlet = LanguageSelectorViewlet(self.context, self.request, self, None)
          viewlet.update()
          result = []
          for lang in viewlet.languages():
              result.append(
                  {"lang": lang['code'].upper(),
                   "url": lang['url'],
                   "active": lang['selected'] and 'is_active' or ''})

          return {"languages": result}

      def render(self):
          return self.hbs_snippet(filename='langswitcher.hbs')

A handlebar tile: ::

    class ContactPersonTile(HandlebarTile):

        def get_contents(self):
            """ Get CMS data and put it in a JSON format
            """

            return {
                'fullname': u'George Miller',
                'phone': '+1 50 206 67 99',
                'email': 'george@example.com',
            }

And the according configure.zcml: ::

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:plone="http://namespaces.plone.org/plone"
        i18n_domain="fhnw.contentwidgets">

      <include package="plone.app.mosaic" />

      <plone:tile
          name="myproduct.contactpersontile"
          title="ContactPerson"
          description="A card of a person"
          add_permission="cmf.ModifyPortalContent"
          class=".tiles.ContactPersonTile"
          for="*"
          permission="zope.Public"
          schema=".tiles.ContactPersonTile"
          template="contactperson.hbs"
      />
    </configure>


Documentation
-------------

Full documentation for end users can be found in the "docs" folder.

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
- Documentation: https://github.com/collective/collective.handlebars/docs


License
-------

The project is licensed under the GPLv2.

