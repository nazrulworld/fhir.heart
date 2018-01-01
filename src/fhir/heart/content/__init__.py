# -*- coding: utf-8 -*-
# @Date    : 2018-01-01 19:33:37
# @Author  : Md Nazrul Islam (email2nazrul@gmail.com)
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from fhir.heart.schema import IHealthcareService
from fhir.heart.schema import IJWTBearerToken
from fhir.heart.schema import IOAuth2Application
from fhir.heart.schema import IOrganization
from fhir.heart.schema import IPatient
from fhir.heart.schema import IPerson
from fhir.heart.schema import IPractitioner
from plone.dexterity.content import Container
from plone.dexterity.content import Item
from zope.interface import implementer


__author__ = 'Md Nazrul Islam (email2nazrul@gmail.com)'


@implementer(IHealthcareService)
class HealthcareService(Item):
    """ """


@implementer(IOrganization)
class Organization(Container):
    """ """


@implementer(IJWTBearerToken)
class JWTBearerToken(Item):
    """ """


@implementer(IOAuth2Application)
class OAuth2Application(Item):
    """ """


@implementer(IPatient)
class Patient(Container):
    """ """


@implementer(IPerson)
class Person(Item):
    """ """


@implementer(IPractitioner)
class Practitioner(Item):
    """ """


__all__ = [str(x) for x in (
    'HealthcareService',
    'Organization',
    'JWTBearerToken',
    'OAuth2Application',
    'Patient',
    'Person',
    'Practitioner')]
