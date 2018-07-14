# -*- coding: utf-8 -*-
# @Date    : 2017-10-07 15:16:29
# @Author  : Md Nazrul Islam (email2nazrul@gmail.com)
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from dexterity.membrane.content.member import IEmail
from fhir.heart import _
from plone.app.fhirfield import FhirResource
from zope import schema


__author__ = 'Md Nazrul Islam (email2nazrul@gmail.com)'


class IBaseUser(IEmail):
    """"Users based on administration resources.
    https://www.hl7.org/fhir/patient.html
    https://www.hl7.org/fhir/practitioner.html
    https://www.hl7.org/fhir/person.html"""
    first_name = schema.TextLine(
        title=_('First Name'),
    )
    last_name = schema.TextLine(
        title=_('Last name')
        )
    mfa = schema.Choice(
        title=_('Multi-factor authentication (MFA)'),
        required=False,
        vocabulary='mfa_types'
        )


class IPatient(IBaseUser):
    """" """
    resource = FhirResource(
        title=_('Patient'),
        resource_type='Patient',
        model_interface='plone.app.fhirfield.interfaces.IFhirResourceModel',
        required=True
        )


class IPractitioner(IBaseUser):
    """" """
    resource = FhirResource(
        title=_('Practitioner'),
        resource_type='Practitioner',
        model_interface='plone.app.fhirfield.interfaces.IFhirResourceModel',
        required=True
        )


class IPerson(IBaseUser):
    """" """
    resource = FhirResource(
        title=_('Person'),
        resource_type='Person',
        model_interface='plone.app.fhirfield.interfaces.IFhirResourceModel',
        required=True
        )
