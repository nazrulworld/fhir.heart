# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from fhir.heart.testing import FHIR_HEART_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that fhir.heart is properly installed."""

    layer = FHIR_HEART_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if fhir.heart is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'fhir.heart'))

    def test_browserlayer(self):
        """Test that IFhirHeartLayer is registered."""
        from fhir.heart.interfaces import (
            IFhirHeartLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IFhirHeartLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = FHIR_HEART_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['fhir.heart'])

    def test_product_uninstalled(self):
        """Test if fhir.heart is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'fhir.heart'))

    def test_browserlayer_removed(self):
        """Test that IFhirHeartLayer is removed."""
        from fhir.heart.interfaces import \
            IFhirHeartLayer
        from plone.browserlayer import utils
        self.assertNotIn(
           IFhirHeartLayer,
           utils.registered_layers())
