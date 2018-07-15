# -*- coding: utf-8 -*-
# @Date    : 2018-01-28 09:58:51
# @Author  : Md Nazrul Islam (email2nazrul@gmail.com)
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from .helpers import BaseFunctionalTest
from .helpers import BaseIntegrationTest
from .helpers import FHIR_RESOURCE_DIRECTORY
from fhir.heart.schema import IOrganization
from plone import api
from plone.dexterity.utils import createContentInContainer
from zope.schema import getFields

import copy


__author__ = 'Md Nazrul Islam (email2nazrul@gmail.com)'


class OrganizationIntegrationTest(BaseIntegrationTest):
    """Test that fhir.heart is properly installed."""

    def test_organization_type_is_available(self):
        """ """
        portal_type = 'Organization'
        portal_types = api.portal.get_tool('portal_types')
        self.assertIn(portal_type, portal_types.listTypeTitles().keys())

        type_info = portal_types.getTypeInfo(portal_type)
        self.assertIsNotNone(type_info)
        # two behaviors
        # self.assertEqual(len(type_info.behaviors), 2)

    def test_add(self):
        """ """
        portal_type = 'Organization'
        data = {
            'id': None,  # we want auto generated ID
            'title': 'Test hospital',
            'description': 'my hospital',

        }
        json_file = FHIR_RESOURCE_DIRECTORY / 'Organization' / 'Organization.json'
        with open(str(json_file), 'r') as f:
            data['organization_resource'] = getFields(IOrganization).get('organization_resource').fromUnicode(f.read())

        with api.env.adopt_roles('Manager'):
            hospital = createContentInContainer(self.portal, portal_type, **data)
        self.assertEqual(hospital.getTypeInfo().factory, portal_type)


class OrganizationFunctionalTest(BaseFunctionalTest):
    """Test"""

    def test_add(self):
        """Test organization is addable."""
        browser = copy.copy(self.admin_browser)
        self.error_setup(browser)
        json_file = FHIR_RESOURCE_DIRECTORY / 'Organization' / 'Organization.json'

        with open(str(json_file), 'r') as f:
            fhir_str = f.read().strip()

        browser.open(self.portal.absolute_url() + '/++add++Organization')
        # browser.getControl(name='form.widgets.IHeartIdChooser.id').value = 'cmo-ltd'
        browser.getControl(name='form.widgets.IBasic.title').value = 'CMO LTD'
        browser.getControl(name='form.widgets.organization_resource').value = fhir_str
        browser.getControl(name='form.buttons.save').click()

        # make sure challenge
        self.assertIn('200', browser.headers['status'])
        # self.assertIn('cmo-ltd', browser.url)
        with open('/tmp/histoty.html', 'w') as f:
            f.write(browser.contents)
