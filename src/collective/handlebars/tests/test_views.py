# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.handlebars.testing import COLLECTIVE_HANDLEBARS_INTEGRATION_TESTING  # noqa
from collective.handlebars.browser.views import HandlebarsBrowserView
from collective.handlebars.browser.views import HandlebarTile

from plone import api
import os.path


import unittest


TEST_DATA__DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'data')


class DummyHbsTile(HandlebarTile):

    def get_contents(self):
        return {'src': 'foo', 'alt': 'bar'}


class DummyHbsTemplate(object):

    def __init__(self, filename):
        self.filename = filename


class TestBrowserView(unittest.TestCase):
    """Test that collective.handlebars is properly installed."""

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
        """Test if collective.handlebars is installed."""
        view = HandlebarsBrowserView(self.portal, self.layer['request'])
        self.assertEqual(view(), '')

    def test_example_view(self):
        """Test that a handlebars template is rendered."""
        view = self.portal.restrictedTraverse('@@hbs_test_view')
        result_file = open(os.path.join(TEST_DATA__DIR, 'minimal.html'))
        self.assertEqual(view(), unicode(result_file.read(), encoding='utf-8'))


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
        self.tile = HandlebarTile(self.layer['portal'], self.layer['request'])
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
        self.assertEqual(self.tile(), '')  # no template referenced in zcml

    def test_call_with_template(self):
        tile = DummyHbsTile(self.layer['portal'], self.layer['request'])
        setattr(tile, 'index', DummyHbsTemplate(self.template_path))
        self.assertEqual(tile().strip(), u'<img src="foo" alt="bar">')
