# -*- coding: utf-8 -*-
# @Date    : 2017-10-04 18:11:14
# @Author  : Md Nazrul Islam (email2nazrul@gmail.com)
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from collections import defaultdict
from collective.fhir.heart import _
from collective.fhir.heart.interfaces import IOAuthClientConfiguration
from collective.fhir.heart.interfaces import IOAuthProviderConfiguration
from collective.fhir.heart.interfaces import IOAuthServerConfiguration
from zope.interface import implementer

import zope.component


try:
    from zope.component.security import PublicPermission
except ImportError:
    # BBB for Zope 2.10
    from zope.component.zcml import PublicPermission

__author__ = 'Md Nazrul Islam (email2nazrul@gmail.com)'


class BaseConfiguration(object):
    """ """

    __slots__ = ('__storage__', '__factory_settings__')

    def __init__(self, settings):
        """ """
        object.__setattr__(self, '__storage__', defaultdict())
        object.__storage__.update(settings)

        object.__setattr__(self, '__factory_settings__', object.__storage__)
        # Might be check, if anything is exist on regisitry?

    def get(self, key, default='___'):
        """"""

        try:
            return self.__storage__[key]
        except KeyError:
            if default == '___':
                raise KeyError(
                    _('{0} is not valid configuration name for {1}').format(key, self.__class__)
                )
            return default

    def set(self, key, value):

        """"""
        set.update(key=value)

    def update(self, **kwargs):

        """ """
        new_items = list()

        for key in kwargs.keys():
            if key not in self.__storage__.keys():
                # @TODO: might need validation first for new key (make sure no unexpected key)
                # could compare with metadirective schema.
                new_items.append(key)

        self.__storage__.update(kwargs)

    def factory_reset(self):
        """Point to first entry"""
        self.__storage__ = self.__factory_settings__

    def clear(self):
        """ """
        self.__storage__.clear()


@implementer(IOAuthClientConfiguration)
class OAuthClientConfiguration(BaseConfiguration):
    """ """


@implementer(IOAuthProviderConfiguration)
class OAuthProviderConfiguration(BaseConfiguration):
    """ """


@implementer(IOAuthServerConfiguration)
class OAuthServerConfiguration(BaseConfiguration):

    """ """


def client_meta_configure(_context, **kwargs):
    """ """
    settings = defaultdict(**kwargs)

    # Validation here

    # Normalized Value here (i.e dotted path to object)

    # Set Default Value (those are missing)

    # Now register utilty
    zope.component.zcml.utility(
        _context,
        provides=IOAuthClientConfiguration,
        component=OAuthClientConfiguration(settings),
        permission=PublicPermission
    )


def provider_meta_configure(_context, **kwargs):
    """ """
    settings = defaultdict(**kwargs)

    # Validation here

    # Normalized Value here (i.e dotted path to object)

    # Set Default Value (those are missing)

    # Now register utilty
    zope.component.zcml.utility(
        _context,
        provides=IOAuthProviderConfiguration,
        component=OAuthProviderConfiguration(settings),
        permission=PublicPermission
    )


def server_meta_configure(_context, **kwargs):
    """ """
    settings = defaultdict(**kwargs)

    # Validation here

    # Normalized Value here (i.e dotted path to object)

    # Set Default Value (those are missing)

    # Now register utilty
    zope.component.zcml.utility(
        _context,
        provides=IOAuthServerConfiguration,
        component=OAuthServerConfiguration(settings),
        permission=PublicPermission
    )
