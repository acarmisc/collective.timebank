# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.timebank.testing import COLLECTIVE_TIMEBANK_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.timebank is properly installed."""

    layer = COLLECTIVE_TIMEBANK_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.timebank is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.timebank'))

    def test_browserlayer(self):
        """Test that ICollectiveTimebankLayer is registered."""
        from collective.timebank.interfaces import (
            ICollectiveTimebankLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectiveTimebankLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_TIMEBANK_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.timebank'])

    def test_product_uninstalled(self):
        """Test if collective.timebank is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.timebank'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveTimebankLayer is removed."""
        from collective.timebank.interfaces import ICollectiveTimebankLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveTimebankLayer, utils.registered_layers())
