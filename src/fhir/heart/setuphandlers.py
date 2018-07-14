# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from Products.membrane.config import TOOLNAME
from zope.interface import implementer


__author__ = '<email2nazrul@gamil.com>'


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'fhir.heart:uninstall',
        ]


def register_membrane_based_portal_types(portal):
    """ """
    allowed_types = ('Patient', 'Person', 'Practitioner', )
    membrane_tool = api.portal.get_tool(TOOLNAME)
    existing_mem_types = set(membrane_tool.listMembraneTypes())

    for portal_type in allowed_types:
        if portal_type not in existing_mem_types:
            membrane_tool.registerMembraneType(portal_type)


def unregister_membrane_based_portal_types(portal):
    """ """
    allowed_types = ('Patient', 'Person', 'Practitioner', )
    membrane_tool = api.portal.get_tool(TOOLNAME)
    existing_mem_types = set(membrane_tool.listMembraneTypes())

    for portal_type in allowed_types:
        if portal_type in existing_mem_types:
            membrane_tool.unregisterMembraneType(portal_type)


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    portal = aq_parent(context)

    # Register FHIR User types into Membrane
    register_membrane_based_portal_types(portal)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
    portal = aq_parent(context)

    # Unregister FHIR User as portal types are removed during uninstall
    unregister_membrane_based_portal_types(portal)
