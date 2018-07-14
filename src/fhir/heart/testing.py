# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import fhir.heart


class FhirHeartLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        z2.installProduct(app, 'Products.membrane')

        import plone.restapi
        self.loadZCML(package=plone.restapi)

        import plone.app.fhirfield
        self.loadZCML(package=plone.app.fhirfield)

        import Products.membrane
        self.loadZCML(package=Products.membrane)

        import dexterity.membrane
        self.loadZCML(package=dexterity.membrane)

        self.loadZCML(package=fhir.heart)

    def setUpPloneSite(self, portal):
        """ """
        applyProfile(portal, 'Products.membrane:default')
        applyProfile(portal, 'dexterity.membrane:default')
        applyProfile(portal, 'plone.restapi:default')
        applyProfile(portal, 'fhir.heart:default')


FHIR_HEART_FIXTURE = FhirHeartLayer()


FHIR_HEART_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FHIR_HEART_FIXTURE,),
    name='FhirHeartLayer:IntegrationTesting'
)


FHIR_HEART_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FHIR_HEART_FIXTURE,),
    name='FhirHeartLayer:FunctionalTesting'
)


FHIR_HEART_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        FHIR_HEART_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='FhirHeartLayer:AcceptanceTesting'
)
