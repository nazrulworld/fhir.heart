# -*- coding: utf-8 -*-
# @Date    : 2017-10-07 15:16:29
# @Author  : Md Nazrul Islam (email2nazrul@gmail.com)
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from fhir.heart.i18n import _
from plone.app.fhirfield import FhirResource
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model


__author__ = 'Md Nazrul Islam (email2nazrul@gmail.com)'


class IOrganization(model.Schema):
    """"Organization resource.
    https://www.hl7.org/fhir/organization.html"""
    resource = FhirResource(
        title=_('FHIR JSON'),
        resource_type='Organization',
        model_interface='plone.app.fhirfield.interfaces.IFhirResourceModel',
        required=True
        )


class IHealthcareService(model.Schema):
    """"HealthcareService resource.
    https://www.hl7.org/fhir/healthcareservice.html"""
    resource = FhirResource(
        title=_('FHIR JSON'),
        resource_type='HealthcareService',
        model_interface='plone.app.fhirfield.interfaces.IFhirResourceModel',
        required=True
        )
    photo = NamedBlobImage(
        title=_('healthcareservice picture'),
        description=_('Photo of organization that link will be attached into resource json'),
        required=False
    )
