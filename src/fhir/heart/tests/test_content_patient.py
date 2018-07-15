# -*- coding: utf-8 -*-
# @Date    : 2018-01-28 09:58:51
# @Author  : Md Nazrul Islam (email2nazrul@gmail.com)
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from .helpers import BaseFunctionalTest
from .helpers import BaseIntegrationTest
from .helpers import FHIR_RESOURCE_DIRECTORY
from fhir.heart.utils import generate_content_id
from fhir.heart.schema import IPatient
from fhir.heart.schema import IOrganization
from plone import api
from plone.dexterity.utils import createContentInContainer
from plone.testing import z2
from zope.schema import getFields

import copy


__author__ = 'Md Nazrul Islam (email2nazrul@gmail.com)'


class OrganizationIntegrationTest(BaseIntegrationTest):
    """Test that fhir.heart is properly installed."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        super(OrganizationIntegrationTest, self).setUp()
        self.make_structure()

    def test_patient_type_is_available(self):
        """ """
        portal_type = 'Patient'
        portal_types = api.portal.get_tool('portal_types')
        self.assertIn(portal_type, portal_types.listTypeTitles().keys())

        type_info = portal_types.getTypeInfo(portal_type)
        self.assertIsNotNone(type_info)
        # two behaviors
        self.assertEqual(len(type_info.behaviors), 4)

    def make_structure(self):
        """ """
        portal_type = 'Organization'
        data = {
            'id': generate_content_id(portal_type),  # we want auto generated ID
            'title': 'Test Healthcare Consortium',
            'description': 'a group of companies based on USA',

        }
        json_file = FHIR_RESOURCE_DIRECTORY / 'Organization' / 'Organization.json'
        with open(str(json_file), 'r') as f:
            data['organization_resource'] = getFields(IOrganization).get('organization_resource').fromUnicode(f.read())

        with api.env.adopt_roles('Manager'):
            self.hospital = createContentInContainer(self.portal, portal_type, **data)

    def test_add(self):
        """ """
        portal_type = 'Patient'
        data = {
            'id': generate_content_id(portal_type),
            'first_name': 'Dr. Byn',
            'last_name': 'Krogh',
            'email': 'test@example.com',
            'username': 'test@example.com',
            'password': '12345',
            'confirm_password': '12345'

        }
        json_file = FHIR_RESOURCE_DIRECTORY / 'Patient' / 'Patient.json'
        with open(str(json_file), 'r') as f:
            data['patient_resource'] = getFields(IPatient).get('patient_resource').fromUnicode(f.read())

        with api.env.adopt_roles('Manager'):
            patient = createContentInContainer(self.hospital, portal_type, **data)

        self.assertEqual(patient.getTypeInfo().factory, portal_type)


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

