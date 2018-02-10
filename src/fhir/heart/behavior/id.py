# -*- coding: utf-8 -*-
# @Date    : 2018-02-04 15:25:53
# @Author  : Md Nazrul Islam (email2nazrul@gmail.com)
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from fhir.heart.i18n import _
from fhir.heart.utils import generate_content_id
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.locking.interfaces import ILockable
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider

import transaction


__author__ = 'Md Nazrul Islam (email2nazrul@gmail.com)'


class IProvideHeartIdChooser(model.Schema):
    """ """
    id = schema.ASCIILine(
        title=_(u'Short name'),
        description=_(u'This name will be displayed in the URL. keep blank for auto generated ID'),
        required=False,
    )


@provider(IFormFieldProvider)
class IHeartIdChooser(IProvideHeartIdChooser):
    """ """
    model.fieldset(
        'settings',
        label=_(u"Settings"),
        fields=['id'],
    )
    directives.write_permission(id='cmf.AddPortalContent')


@implementer(IProvideHeartIdChooser)
@adapter(IDexterityContent)
class HeartId(object):
    """ """
    def __init__(self, context):
        self.context = context

    def _get_id(self):
        return self.context.getId()

    def _set_id(self, value):
        """ """
        context = aq_inner(self.context)
        parent = aq_parent(context)
        if not value:
            # plone.dexterity.fti.DexterityFTI
            factory_info = context.getTypeInfo()
            new_id = generate_content_id(factory_info.getId())
        # else add prefix/suffix with user provided value?
        else:
            new_id = value

        if parent is None:
            # Object hasn't been added to graph yet; just set directly
            context.id = value
            return

        if getattr(aq_base(context), 'id', None):
            transaction.savepoint()
            locked = False
            lockable = ILockable(context, None)
            if lockable is not None and lockable.locked():
                locked = True
                lockable.unlock()
            parent.manage_renameObject(context.getId(), new_id)
            if locked:
                lockable.lock()
        else:
            context.id = new_id
    id = property(_get_id, _set_id)
