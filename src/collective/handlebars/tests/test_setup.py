# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.handlebars.testing import COLLECTIVE_HANDLEBARS_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.handlebars is properly installed."""

    layer = COLLECTIVE_HANDLEBARS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.handlebars is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.handlebars'))

    def test_browserlayer(self):
        """Test that ICollectiveHandlebarsLayer is registered."""
        from collective.handlebars.interfaces import (
            ICollectiveHandlebarsLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectiveHandlebarsLayer, utils.registered_layers())


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

    def test_hiddenprofiles(self):
        """ Test uninstall profile is hidden
        :return:None
        """
        from collective.handlebars.setuphandlers import HiddenProfiles
        self.assertIn('collective.handlebars:default',
                      HiddenProfiles().getNonInstallableProfiles())
        self.assertIn('collective.handlebars:uninstall',
                      HiddenProfiles().getNonInstallableProfiles())
