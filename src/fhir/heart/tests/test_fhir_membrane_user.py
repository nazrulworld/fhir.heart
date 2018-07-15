# -*- coding: utf-8 -*-
# @Date    : 2018-07-15 16:44:09
# @Author  : Md Nazrul Islam (email2nazrul@gmail.com)
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from .helpers import BaseIntegrationTest
from .helpers import FHIR_RESOURCE_DIRECTORY
from plone import api
from plone.uuid.interfaces import IUUID
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from fhir.heart.compat import json
from fhir.heart.schema import IPatient
from zope.schema import getFields
from zope.component import queryMultiAdapter
from plone.restapi.interfaces import IDeserializeFromJson

import uuid


__author__ = 'Md Nazrul Islam (email2nazrul@gmail.com)'


class FhirMembraneUserIntegrationTest(BaseIntegrationTest):
    """Test all membrane based users are
    using in this product"""

    def get_hospital(self):
        """ """
        query = api.content.find(portal_type='Organization', sort_limit=1)
        return query[0].getObject()

    def test_patient_user(self):
        """ """
        setRoles(self.portal, TEST_USER_ID, ['Manager', ])
        with open(str(FHIR_RESOURCE_DIRECTORY / 'Patient' / 'Patient.json'), 'r') as f:  # noqa: E501
            fhir_json = json.load(f)

        container = self.get_hospital()

        patient = api.content.create(
            container,
            'Patient',
            id=str(uuid.uuid4()),
            title=' '.join(fhir_json['name'][0]['given']),
            safeid=False,
            )
        import pdb;pdb.set_trace()
        data = dict(
            email='one@example.com',
            password='12345',
            confirm_password='12345',
            first_name='First Patient',
            last_name='Krogh',
            patient_resource=fhir_json)

        request = self.portal.REQUEST.clone()
        request['BODY'] = json.dumps(data)

        deserializer = queryMultiAdapter((patient, request), IDeserializeFromJson)
        deserializer(validate_all=True)

        api.content.transition(obj=patient, to_state='enabled')

        user = api.user.get(username=data['email'])

        self.assertIsNotNone(user)
        # By default user id = object UUID
        self.assertEqual(user.getUserId(), IUUID(patient))
