# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.handlebars.testing import (
    COLLECTIVE_HANDLEBARS_INTEGRATION_TESTING,
)
from plone import api

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:  # pragma: no cover
    # Quick shim for 5.1 api change

    class get_installer(object):  # noqa
        def __init__(self, portal, request):  # noqa
            self.installer = api.portal.get_tool(name="portal_quickinstaller")

        def is_product_installed(self, name):
            return self.installer.isProductInstalled(name)

        def uninstall_product(self, name):
            return self.installer.uninstallProducts([name])


class TestSetup(unittest.TestCase):
    """Test that collective.handlebars is properly installed."""

    layer = COLLECTIVE_HANDLEBARS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if collective.handlebars is installed."""
        self.assertTrue(
            self.installer.is_product_installed("collective.handlebars")
        )

    def test_browserlayer(self):
        """Test that ICollectiveHandlebarsLayer is registered."""
        from collective.handlebars.interfaces import ICollectiveHandlebarsLayer
        from plone.browserlayer import utils

        self.assertIn(ICollectiveHandlebarsLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_HANDLEBARS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        self.installer.uninstall_product("collective.handlebars")

    def test_product_uninstalled(self):
        """Test if collective.handlebars is cleanly uninstalled."""
        self.assertFalse(
            self.installer.is_product_installed("collective.handlebars")
        )

    def test_browserlayer_removed(self):
        """Test that ICollectiveHandlebarsLayer is removed."""
        from collective.handlebars.interfaces import ICollectiveHandlebarsLayer
        from plone.browserlayer import utils

        self.assertNotIn(ICollectiveHandlebarsLayer, utils.registered_layers())

    def test_hiddenprofiles(self):
        """Test uninstall profile is hidden
        :return:None
        """
        from collective.handlebars.setuphandlers import HiddenProfiles

        self.assertIn(
            "collective.handlebars:default",
            HiddenProfiles().getNonInstallableProfiles(),
        )
        self.assertIn(
            "collective.handlebars:uninstall",
            HiddenProfiles().getNonInstallableProfiles(),
        )
