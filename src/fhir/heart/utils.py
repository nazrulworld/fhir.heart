# _*_ coding: utf-8 _*_
from Acquisition import aq_inner
from Acquisition import aq_parent
from plone import api
from plone.api.validation import at_least_one_of
from plone.api.validation import mutually_exclusive_parameters
from plone.api.validation import required_parameters
from Products.CMFCore.utils import getToolByName
from zope.schema import getFields

import six
import time


__author__ = 'Md Nazrul Islam<email2nazrul@gmail.com>'


@required_parameters('value')
def force_unicode(value, allow_non_str=True):
    """ """
    if not isinstance(value, six.string_types):
        if not allow_non_str:
            return value
        else:
            value = str(value)

    if isinstance(value, bytes):
        return value.decode('utf-8', 'strict')

    if six.PY2:
        if not isinstance(value, unicode):
            return value.decode('utf-8', 'strict')

    return value


@required_parameters('string')
def force_bytes(string, encoding='utf-8', errors='strict'):

    if isinstance(string, bytes):
        if encoding == 'utf-8':
            return string
        else:
            return string.decode('utf-8', errors).encode(encoding, errors)

    if not isinstance(string, six.string_types):
        return string

    return string.encode(encoding, errors)


def generate_content_id(content_name):
    """ """
    parts = '{0!r}'.format(time.time()).split('.')
    # dash(-) is url friendly
    id_ = '-'.join([
        content_name.lower(),
        hex(int(parts[0])).encode('utf-8')[2:],
        str(parts[1])
        ])
    return id_


@mutually_exclusive_parameters('userid', 'username')
@at_least_one_of('userid', 'username')
def get_userfolder(userid=None, username=None, context=None):
    """Try to find a user folder that contains a user with the given
       userid.
    """
    context = context or api.portal.get()
    uf_parent = aq_inner(context)
    info = None

    while not info:
        uf = getToolByName(uf_parent, 'acl_users')  # noqa: P001
        if uf:
            if userid:
                param = {'user_id': userid}
            else:
                param = {'login': username}

            info = uf._verifyUser(uf.plugins, **param)
        if uf_parent is context.getPhysicalRoot():
            break
        uf_parent = aq_parent(uf_parent)

    if info:
        return uf
    return None


@mutually_exclusive_parameters('username', 'user')
@at_least_one_of('username', 'user')
def get_user_id(username=None, user=None):
    """ """
    if username:
        user = api.user.get(username=username)

    try:
        userid = user.getUserId()
    except AttributeError:
        userid = user.getId()

    return userid


@at_least_one_of('obj', 'portal_type')
@mutually_exclusive_parameters('obj', 'portal_type')
def get_fhir_field(obj=None, portal_type=None):
    """Extract FHIR field's value from object """

    if obj:
        fhir_field_name = '{0}_resource'.format(obj.getTypeInfo().getId().lower())
        fields = getFields(obj.getTypeInfo().lookupSchema())
    elif portal_type:
        fhir_field_name = '{0}_resource'.format(portal_type.lower())
        fti = api.portal.get_tool('portal_types').get(portal_type, None)
        assert fti is not None
        fields = getFields(fti.lookupSchema())

    fhir_field = fields.get(fhir_field_name, None)
    if fhir_field is None:
        fhir_field = fields.get('resource')

    # make sure fhir field should exists
    return fhir_field


@required_parameters('obj')
def get_fhir_value(obj):
    """Extract FHIR field's value from object """
    fhir_field = get_fhir_field(obj)

    return getattr(obj, fhir_field.getName())
