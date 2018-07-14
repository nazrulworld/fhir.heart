# -*- coding: utf-8 -*-
# @Date    : 2018-01-21 14:52:53
# @Author  : Md Nazrul Islam (email2nazrul@gmail.com)
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from .utils import force_unicode
from fhir.heart import _
from plone import api
from plone.api.validation import mutually_exclusive_parameters
from plone.api.validation import required_parameters
from zope.globalrequest import getRequest
from zope.i18n import translate as zt
from zope.i18nmessageid import Message
from zope.interface import Invalid


__author__ = 'Md Nazrul Islam (email2nazrul@gmail.com)'


@mutually_exclusive_parameters('user', 'username', 'userid')
def get_user_language(user=None, username=None, userid=None):
    """ """
    if user is None:
        if username:
            user = api.user.get(username=username)
        elif userid:
            user = api.user.get(userid=userid)

        if user is None:
            raise Invalid(
                'No user found associated with {0}!'.
                format(username or userid))

    if user is None:
        user = api.user.get_current()

    language = user.getProperty('language', '')

    if not language:
        language = getRequest().get_header('Accept-Language', '')

    if not language:
        language = api.portal.get_current_language()

    return language


@required_parameters('message')
def translate(message, target_language=None, mapping=None):
    """zope.i18n translation implementation with control way """
    if not isinstance(message, Message) and mapping:
        """ """
        message = _(force_unicode(message), mapping=mapping)

    target_language = target_language or get_user_language()
    return zt(message, target_language=target_language, mapping=mapping)
