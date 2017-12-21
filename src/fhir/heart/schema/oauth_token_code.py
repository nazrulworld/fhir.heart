# -*- coding: utf-8 -*-
# @Date    : 2017-10-12 19:34:26
# @Author  : Md Nazrul Islam (email2nazrul@gmail.com)
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from collective.fhir.heart import _
from plone.supermodel import model
from zope import schema as zs
from zope.interface import Invalid
from zope.interface import invariant

import json

__author__ = 'Md Nazrul Islam (email2nazrul@gmail.com)'


class ITokenCodeBase(model.Schema):
    """ """
    user_id = zs.TextLine(
        title=_('User\'s ID'),
        required=True
    )
    client_id = zs.TextLine(
        title=_('Application ID'),
        required=True
    )
    scope = zs.List(
        title=_('List of scopes'),
        required=False,
        value_type=zs.TextLine()
    )
    expire_at = zs.DateTime(
        title=_('Token Expire Date'),
        required=True
    )

    @invariant
    def validate_existance(self, data):
        """Validate if User and Application Is exists"""
        return Invalid('')


class IJWTBearerToken(ITokenCodeBase):
    """ """
    access_token = zs.TextLine()
    refresh_token = zs.TextLine()
    _id_token = zs.TextLine()

    def id_token():

        def fget(self):
            return json.loads(self._id_token)

        def fset(self, value):
            self._id_token = json.dumps(value)

        return locals()
    id_token = property(**id_token())