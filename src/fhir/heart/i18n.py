# -*- coding: utf-8 -*-
# @Date    : 2018-01-21 14:52:53
# @Author  : Md Nazrul Islam (email2nazrul@gmail.com)
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from plone import api
from zope.globalrequest import getRequest
from zope.i18n import translate as zt
from zope.i18nmessageid import Message
from zope.i18nmessageid import MessageFactory


__author__ = 'Md Nazrul Islam (email2nazrul@gmail.com)'

_ = MessageFactory('fhir.heart')


def get_user_language(user=None):
    """ """
    user = user or api.user.get_current()
    language = user.getProperty('language', None)

    if language is None:
        language = getRequest().get_header('Accept-Language', None)
    if language is None:
        language = api.portal.get_current_language()

    return language


def translate(message, target_language=None):
    """zope.i18n translation implementation with control way """
    if not isinstance(message, Message):
        """ """
        message = _(message)

    target_language = target_language or get_user_language()
    return zt(message, target_language=target_language)