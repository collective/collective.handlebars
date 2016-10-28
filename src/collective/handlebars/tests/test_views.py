# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.handlebars.testing import COLLECTIVE_HANDLEBARS_INTEGRATION_TESTING  # noqa
from collective.handlebars.browser.views import HandlebarsBrowserView
from collective.handlebars.browser.views import HandlebarsTile
from collective.handlebars.browser.views import HandlebarsPersistentTile

from plone import api
from zope.i18nmessageid import MessageFactory
from zope import component, interface
from zope.i18n.interfaces import ITranslationDomain
import os.path

import unittest


TEST_DATA__DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'data')
_ = MessageFactory('my.domain')


class DummyHbsTile(HandlebarsTile):

    def get_contents(self):
        return {'src': 'foo', 'alt': 'bar'}


class DummyHbsPersistentTile(HandlebarsPersistentTile):

    def get_contents(self):
        return {'src': 'foo', 'alt': 'bar'}


class DummyHbsTemplate(object):

    def __init__(self, filename):
        self.filename = filename


@interface.implementer(ITranslationDomain)
class TestDomain(dict):

    def translate(self, text, *_, **__):
        return self[text], _[2]


class DummyHbsFile(HandlebarsBrowserView):

    def get_contents(self):
        return {'title': u'File Test',
                'body': u'Hello HBS World!'}

    def __call__(self):
        return self.hbs_snippet('data/minimal.hbs')

    def invalid(self):
        return self.hbs_snippet('data/minimal_notfound.hbs')


class TestBrowserView(unittest.TestCase):
    """Test the collective.handlebars BrowserView component."""

    layer = COLLECTIVE_HANDLEBARS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.view = self.portal.restrictedTraverse('@@hbs_test_view')

    def test_get_contents_default(self):
        """ Method `get_tile_data` is not implemented in base class

        :return:
        """
        view = HandlebarsBrowserView(self.portal, self.layer['request'])
        self.assertRaises(NotImplementedError, view.get_contents)

    def test_base_view(self):
        """ An error is raised, if no template is specified """
        view = HandlebarsBrowserView(self.portal, self.layer['request'])
        self.assertRaises(ValueError, view)

    def test_example_view(self):
        """Test that a handlebars template is rendered."""
        view = self.portal.restrictedTraverse('@@hbs_test_view')
        result_file = open(os.path.join(TEST_DATA__DIR, 'minimal.html'))
        self.assertEqual(view(), unicode(result_file.read(), encoding='utf-8'))

    def test_translate(self):
        view = HandlebarsBrowserView(self.portal, self.layer['request'])
        component.provideUtility(TestDomain(Allowed=_('Erlaubt')),
                                 name='my.domain')
        self.assertEqual(view.translate(_('Allowed'), target_language='de'),
                         (u'Erlaubt', 'de'))

    def test_translate_default_lang(self):
        view = HandlebarsBrowserView(self.portal, self.layer['request'])
        component.provideUtility(TestDomain(Allowed=_('Allowed')),
                                 name='my.domain')
        self.assertEqual(view.translate(_('Allowed')), (u'Allowed', 'en'))

    def test_hbs_snippet(self):
        view = DummyHbsFile(self.portal, self.layer['request'])
        result_file = open(os.path.join(TEST_DATA__DIR, 'minimal_file.html'))
        self.assertEqual(view(), unicode(result_file.read(), encoding='utf-8'))

    def test_hbs_snippet_nofile(self):
        view = DummyHbsFile(self.portal, self.layer['request'])
        self.assertRaises(ValueError, view.invalid)

    def test_get_path_from_prefix(self):
        view = DummyHbsFile(self.portal, self.layer['request'])
        self.assertEqual(view.get_path_from_prefix(_prefix='.'), '.')


class TestPloneView(unittest.TestCase):
    """Test the collective.handlebars BrowserView component."""

    layer = COLLECTIVE_HANDLEBARS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.view = self.portal.restrictedTraverse('@@hbs_test_ploneview')

    def test_get_contents_default(self):
        """ Method `get_tile_data` is not implemented in base class

        :return:
        """
        view = HandlebarsBrowserView(self.portal, self.layer['request'])
        self.assertRaises(NotImplementedError, view.get_contents)

    def test_base_view(self):
        """ An error is raised, if no template is specified """
        view = HandlebarsBrowserView(self.portal, self.layer['request'])
        self.assertRaises(ValueError, view)

    def test_example_view(self):
        """Test that a handlebars template is rendered."""
        view = self.portal.restrictedTraverse('@@hbs_test_ploneview')
        result_file = open(os.path.join(TEST_DATA__DIR, 'minimal_plone.html'))
        self.assertIn(unicode(result_file.read(), encoding='utf-8'), view())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_HANDLEBARS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.handlebars'])

    def test_product_uninstalled(self):
        """Test if collective.handlebars is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.handlebars'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveHandlebarsLayer is removed."""
        from collective.handlebars.interfaces import ICollectiveHandlebarsLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveHandlebarsLayer, utils.registered_layers())


class TestHandlebarTile(unittest.TestCase):
    """Test that fhnw.web16theme viewlets."""

    layer = COLLECTIVE_HANDLEBARS_INTEGRATION_TESTING

    def setUp(self):
        self.tile = HandlebarsTile(self.layer['portal'], self.layer['request'])
        self.template_path = os.path.join(TEST_DATA__DIR,
                                          '_slideshow_slide.js.hbs')

    def test_get_contents_default(self):
        """ Method `get_tile_data` is not implemented in base class

        :return:
        """
        view = HandlebarsBrowserView(self.layer['portal'],
                                     self.layer['request'])
        self.assertRaises(NotImplementedError, view.get_contents)

    def test_get_hbs_template(self):
        template = self.tile._get_hbs_template(self.template_path)
        self.assertEqual(template({'src': 'foo', 'alt': 'bar'}).strip(),
                         u'<img src="foo" alt="bar">')

    def test_get_partial_key(self):
        self.assertEqual(self.tile._get_partial_key(self.template_path),
                         '_slideshow_slide.js')

    def test_call_notemplate(self):
        """ An error is raised, if no template is specified """
        self.assertRaises(ValueError, self.tile)

    def test_call_with_template(self):
        tile = DummyHbsTile(self.layer['portal'], self.layer['request'])
        setattr(tile, 'index', DummyHbsTemplate(self.template_path))
        self.assertEqual(tile().strip(), u'<img src="foo" alt="bar">')


class TestHandlebarPersistentTile(unittest.TestCase):
    """Test that fhnw.web16theme viewlets."""

    layer = COLLECTIVE_HANDLEBARS_INTEGRATION_TESTING

    def setUp(self):
        self.tile = HandlebarsPersistentTile(
            self.layer['portal'], self.layer['request'])
        self.template_path = os.path.join(TEST_DATA__DIR,
                                          '_slideshow_slide.js.hbs')

    def test_get_contents_default(self):
        """ Method `get_tile_data` is not implemented in base class

        :return:
        """
        view = HandlebarsBrowserView(self.layer['portal'],
                                     self.layer['request'])
        self.assertRaises(NotImplementedError, view.get_contents)

    def test_get_hbs_template(self):
        template = self.tile._get_hbs_template(self.template_path)
        self.assertEqual(template({'src': 'foo', 'alt': 'bar'}).strip(),
                         u'<img src="foo" alt="bar">')

    def test_get_partial_key(self):
        self.assertEqual(self.tile._get_partial_key(self.template_path),
                         '_slideshow_slide.js')

    def test_call_notemplate(self):
        """ An error is raised, if no template is specified """
        self.assertRaises(ValueError, self.tile)

    def test_call_with_template(self):
        tile = DummyHbsTile(self.layer['portal'], self.layer['request'])
        setattr(tile, 'index', DummyHbsTemplate(self.template_path))
        self.assertEqual(tile().strip(), u'<img src="foo" alt="bar">')
