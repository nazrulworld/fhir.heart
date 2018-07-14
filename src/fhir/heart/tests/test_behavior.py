# -*- coding: utf-8 -*-
from fhir.heart.behavior.id import IHeartIdChooser
from fhir.heart.behavior.user import IOidConnectClaims
from fhir.heart.testing import FHIR_HEART_INTEGRATION_TESTING
from plone import api
from plone.behavior.interfaces import IBehavior
from plone.dexterity.behavior import DexterityBehaviorAssignable
from zope.component import queryUtility
from zope.interface import Interface

import unittest


__author__ = 'Md Nazrul Islam<email2nazrul@gmail.com>'


class TestBehavior(unittest.TestCase):
    """ """
    layer = FHIR_HEART_INTEGRATION_TESTING

    def setUp(self):
        """ """
        self.portal = self.layer['portal']

    def offtest_defined_behaviors(self):
        """Auto Behavior Name::

            >>> from fhir.heart.behavior.user import IOidConnectClaims
            >>> print IOidConnectClaims.__identifier__
            fhir.heart.behavior.user.IOidConnectClaims
            >>> fhir.heart.behavior.id import IHeartIdChooser
            >>> print  IHeartIdChooser.__identifier__
            fhir.heart.behavior.id.IHeartIdChooser
        """
        oid_connection_claims = queryUtility(IBehavior, name='fhir.heart.behavior.user.IOidConnectClaims')
        self.assertIsNotNone(oid_connection_claims)

        id_chooser = queryUtility(IBehavior, name='fhir.heart.behavior.id.IHeartIdChooser')
        self.assertIsNotNone(id_chooser)

    def offtest_supports(self):
        """ """
        # Context mock
        with api.env.adopt_roles('Manager'):
            id_ = self.portal.invokeFactory('Organization', 'hospital')
            organization_context = self.portal[id_]
            id_ = organization_context.invokeFactory('Patient', 'patient')
            patient_context = organization_context[id_]

        # Test: Organization has IHeartIdChooser but not IOidConnectClaims
        assignable = DexterityBehaviorAssignable(organization_context)
        self.assertEqual(False, assignable.supports(IOidConnectClaims))
        self.assertEqual(True, assignable.supports(IHeartIdChooser))

        # Test: Patient has both behaviors
        assignable = DexterityBehaviorAssignable(patient_context)
        self.assertEqual(True, assignable.supports(IOidConnectClaims))
        self.assertEqual(True, assignable.supports(IHeartIdChooser))

    def offtest_enumerate(self):
        """ """
        with api.env.adopt_roles('Manager'):
            id_ = self.portal.invokeFactory('Organization', 'hospital')
            organization_context = self.portal[id_]
            id_ = organization_context.invokeFactory('Patient', 'patient')
            patient_context = organization_context[id_]

        oid_connection_claims = queryUtility(IBehavior, name=IOidConnectClaims.__identifier__)
        id_chooser = queryUtility(IBehavior, name=IHeartIdChooser.__identifier__)

        assignable = DexterityBehaviorAssignable(organization_context)

        # Organization has IHeartIdChooser
        self.assertIn(
            id_chooser,
            list(assignable.enumerateBehaviors())
        )
        self.assertNotIn(
            oid_connection_claims,
            list(assignable.enumerateBehaviors())
        )

        # Patient has both
        assignable = DexterityBehaviorAssignable(patient_context)
        self.assertIn(
            id_chooser,
            list(assignable.enumerateBehaviors())
        )
        self.assertIn(
            oid_connection_claims,
            list(assignable.enumerateBehaviors())
        )
