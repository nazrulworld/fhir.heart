# -*- coding: utf-8 -*-
# @Date    : 2017-10-12 19:34:26
# @Author  : Md Nazrul Islam (email2nazrul@gmail.com)
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from fhir.heart import _
from fhir.heart.schema.oauth_application import IOAuth2Application
from fhir.heart.schema.user import IBaseUser
from plone.app.jsonfield import JSON
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema as zs
from zope.interface import Invalid
from zope.interface import invariant


__author__ = 'Md Nazrul Islam (email2nazrul@gmail.com)'


class ITokenCodeBase(model.Schema):
    """OID Map:
    :user_id = user
    :client_id = client"""
    user = RelationChoice(
        title=_('User'),
        source=ObjPathSourceBinder(object_provides=IBaseUser.__identifier__),
        required=True
    )
    client = RelationChoice(
        title=_('Application'),
        source=ObjPathSourceBinder(object_provides=IOAuth2Application.__identifier__),
        required=True
    )
    scope = zs.List(
        title=_('List of scopes'),
        required=False,
        value_type=zs.TextLine()
    )
    expire_at = zs.Datetime(
        title=_('Token Expire Date'),
        required=True
    )

    @invariant
    def validate_existance(self, data):
        """Validate if User and Application Is exists"""
        return Invalid('')


class IJWTBearerToken(ITokenCodeBase):
    """ """
    access_token = zs.TextLine(
        title=_('Access token')
        )
    refresh_token = zs.TextLine(
        title=_('Refresh token')
        )
    id_token = JSON(
        title=_('ID Token')
        )
