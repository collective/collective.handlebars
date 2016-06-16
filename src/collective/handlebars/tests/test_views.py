# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.handlebars.testing import COLLECTIVE_HANDLEBARS_INTEGRATION_TESTING  # noqa
from collective.handlebars.browser.views import HandlebarsBrowserView

from plone import api
import os.path


import unittest


TEST_DATA__DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'data')


class TestBrowserView(unittest.TestCase):
    """Test that collective.handlebars is properly installed."""

    layer = COLLECTIVE_HANDLEBARS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.view = self.portal.restrictedTraverse('@@hbs_test_view')

    def test_base_view(self):
        """Test if collective.handlebars is installed."""
        self.assertEqual(HandlebarsBrowserView(self.portal, self.layer['request'])(), '')

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
