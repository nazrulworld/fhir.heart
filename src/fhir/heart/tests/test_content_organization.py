# -*- coding: utf-8 -*-
# @Date    : 2018-01-28 09:58:51
# @Author  : Md Nazrul Islam (email2nazrul@gmail.com)
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from .helpers import STATIC_FHIR_DIRECTORY
from fhir.heart.schema import IOrganization
from fhir.heart.testing import FHIR_HEART_FUNCTIONAL_TESTING
from fhir.heart.testing import FHIR_HEART_INTEGRATION_TESTING
from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.dexterity.utils import createContentInContainer
from plone.testing import z2
from zope.schema import getFields

import copy
import logging
import six
import sys
import unittest


__author__ = 'Md Nazrul Islam (email2nazrul@gmail.com)'


class OrganizationIntegrationTest(unittest.TestCase):
    """Test that fhir.heart is properly installed."""

    layer = FHIR_HEART_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_organization_type_is_available(self):
        """ """
        portal_type = 'Organization'
        portal_types = api.portal.get_tool('portal_types')
        self.assertIn(portal_type, portal_types.listTypeTitles().keys())

        type_info = portal_types.getTypeInfo(portal_type)
        self.assertIsNotNone(type_info)
        # two behaviors
        self.assertEqual(len(type_info.behaviors), 2)

    def test_add(self):
        """ """
        portal_type = 'Organization'
        data = {
            'title': 'Test hospital',
            'description': 'my hospital',

        }
        json_file = STATIC_FHIR_DIRECTORY / 'Organization' / 'Organization.json'
        with open(str(json_file), 'r') as f:
            data['resource'] = getFields(IOrganization).get('resource').fromUnicode(f.read())

        with api.env.adopt_roles('Manager'):
            hospital = createContentInContainer(self.portal, portal_type, **data)
        self.assertEqual(hospital.getTypeInfo().factory, portal_type)


class OrganizationFunctionalTest(unittest.TestCase):
    """Test"""

    layer = FHIR_HEART_FUNCTIONAL_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.admin_browser = z2.Browser(self.layer['app'])
        self.admin_browser.addHeader('Authorization', 'Basic {0}:{1}'.format(SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
        self.anon_browser = z2.Browser(self.layer['app'])

        self.enable_event_log()

    def test_add(self):
        """Test organization is addable."""
        browser = copy.copy(self.admin_browser)
        self.error_setup(browser)
        json_file = STATIC_FHIR_DIRECTORY / 'Organization' / 'Organization.json'

        with open(str(json_file), 'r') as f:
            fhir_str = f.read().strip()

        browser.open(self.portal.absolute_url() + '/++add++Organization')
        browser.getControl(name='form.widgets.IHeartIdChooser.id').value = 'cmo-ltd'
        browser.getControl(name='form.widgets.IBasic.title').value = 'CMO LTD'
        browser.getControl(name='form.widgets.resource').value = fhir_str
        browser.getControl(name='form.buttons.save').click()

        # make sure challenge
        self.assertIn('200', browser.headers['status'])
        self.assertIn('cmo-ltd', browser.url)
        with open('/tmp/histoty.html', 'w') as f:
            f.write(browser.contents)

    def error_setup(self, browser):
        """ """
        browser.handleErrors = False
        self.portal.error_log._ignored_exceptions = ()

        def raising(self, info):
            import traceback
            traceback.print_tb(info[2])
            print (info[1])

        from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
        SiteErrorLog.raising = raising

    def enable_event_log(self, loggers=None, plone_log_level='ERROR'):
        """
            :param loggers: dict of loggers. format {'logger name': 'level name'}
            :param plone_log_level: log level of plone. default is ERROR
         """
        defaults = {
            'fhir.heart': 'INFO'
        }
        from Products.CMFPlone.log import logger

        loggers = loggers or defaults

        for logger_name, level_name in six.iteritems(loggers):
            logging.getLogger(logger_name).setLevel(getattr(logging, level_name.upper()))
        # Plone log level:
        logger.root.setLevel(getattr(logging, plone_log_level.upper()))

        # Enable output when running tests:
        logger.root.addHandler(logging.StreamHandler(sys.stdout))
