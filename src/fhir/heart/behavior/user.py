# -*- coding: utf-8 -*-
# @Date    : 2017-10-07 15:14:27
# @Author  : Md Nazrul Islam (email2nazrul@gmail.com)
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from dexterity.membrane.behavior.user import IMembraneUser
from fhir.heart import _
from plone import schema as ps
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider
from zope.interface import Interface
from Products.membrane.interfaces import IMembraneUserObject


__author__ = 'Md Nazrul Islam (email2nazrul@gmail.com)'


class IOidConnectUser(Interface):
    """Marker/Form interface for Membrane User"""


class IProvideOidConnectClaims(model.Schema):
    """Add OpenID Connect Claims fields.
    http://openid.net/specs/openid-connect-core-1_0.html#Claims
    """

    sub = ps.TextLine(
        title=_('Subject'),
        required=False,
    )

    name = ps.TextLine(
        title=_('Full Name'),
        description=_(
            "End-User's full name in displayable form including all name parts, "
            'possibly including titles and suffixes, '
            "ordered according to the End-User's locale and preferences."
        ),
        required=False,
    )
    given_name = ps.TextLine(
        title=_('First Name'),
        description=_(
            'Given name(s) or first name(s) of the End-User. Note that in some cultures, '
            'people can have multiple given names; all can be present, with the names being '
            'separated by space characters'
        ),
        required=False
    )
    family_name = ps.TextLine(
        title=_('Last Name'),
        description=_(
            'Surname(s) or last name(s) of the End-User. Note that in some cultures, '
            'people can have multiple family names or no family name; all can be present, '
            'with the names being separated by space characters.'
        ),
        required=False
    )
    middle_name = ps.TextLine(
        title=_('Middle Name'),
        description=_(
            'Middle name(s) of the End-User. Note that in some cultures, '
            'people can have multiple middle names; all can be present, '
            'with the names being separated by space characters. '
            'Also note that in some cultures, middle names are not used.'
        ),
        required=False
    )
    nickname = ps.TextLine(
        title=_('Nickname'),
        description=_(
            'Casual name of the End-User that may or may not be the same as the given_name. '
            'For instance, a nickname value of Mike might be returned alongside a given_name '
            'value of Michael.'
        ),
        required=False
    )
    preferred_username = ps.TextLine(
        title=_('Username'),
        description=_(
            'Given name(s) or first name(s) of the End-User. Note that in some cultures, '
            'people can have multiple given names; all can be present, with the names being '
            'separated by space characters'
        ),
        required=False
    )
    profile = ps.URI(
        title=_('Profile URL'),
        description=_(
            "URL of the End-User\'s profile page. "
            'The contents of this Web page SHOULD be about the End-User.'
        ),
        required=False,
    )
    picture = NamedBlobImage(
        title=_('profile picture'),
        description=_(
            "URL of the End-User\'s profile picture. "
            'This URL MUST refer to an image file (for example, a PNG, JPEG, or GIF image file), '
            'rather than to a Web page containing an image. '
            'Note that this URL SHOULD specifically reference a profile photo of the End-User '
            'suitable for displaying when describing the End-User, '
            'rather than an arbitrary photo taken by the End-User.'
        ),
        required=False
    )

    website = ps.URI(
        title=_('Website URL'),
        description=_(
            "URL of the End-User\'s Web page or blog. "
            'This Web page SHOULD contain information published by '
            'the End-User or an organization that the End-User is affiliated with.'
        )
    )
    email_verified = ps.Bool(
        title=_('Id Email Verified'),
        description=_(
            'controlled by the End-User at the time the verification was performed. '
            'The means by which an e-mail address is verified is context-specific, '
            'and dependent upon the trust framework or contractual agreements within '
            'which the parties are operating.'
        ),
        required=False
    )
    gender = ps.Choice(
        title=_('Gender'),
        description=_(
            "End-User's gender. Values defined by this specification are female and male. "
            'Other values MAY be used when neither of the defined values are applicable.'
        ),
        vocabulary='gender_options'
    )

    birthdate = ps.Date(
        title=_('Birth Date'),
        description=_(
            str("End-User's birthday, represented as an ISO 8601:2004 [ISO8601‑2004] ").decode('utf-8') +
            'YYYY-MM-DD format. The year MAY be 0000, indicating that it is omitted. '
            'To represent only the year, YYYY format is allowed. '
            "Note that depending on the underlying platform's date related function, "
            'providing just year can result in varying month and day, '
            'so the implementers need to take this factor into account to '
            'correctly process the dates.'
        ),
        required=True
    )

    zoneinfo = ps.Choice(
        title=_('Time Zone'),
        description=_(
            'String from zoneinfo [zoneinfo] time zone database representing the '
            'End-User\'s time zone. For example, Europe/Paris or America/Los_Angeles.'
        ),
        vocabulary='plone.app.vocabularies.CommonTimezones',
        required=False
    )

    locale = ps.TextLine(
        title=_('Language'),
        description=_(
            str('End-User\'s locale, represented as a BCP47 [RFC5646] language tag. '
            'This is typically an ISO 639-1 Alpha-2 [ISO639‑1] language code in '
            'lowercase and an ISO 3166-1 Alpha-2 [ISO3166‑1] country code in uppercase, ').decode('utf-8') +
            'separated by a dash. For example, en-US or fr-CA. As a compatibility note, '
            'some implementations have used an underscore as the separator rather than a dash, '
            'for example, en_US; Relying Parties MAY choose to accept this locale syntax as well.'
        ),
        required=False
    )
    phone_number = ps.TextLine(
        title=_('Phone Number'),
        description=_(
            'End-User\'s preferred telephone number. '
            'E.164 [E.164] is RECOMMENDED as the format of this Claim, '
            'for example, +1 (425) 555-1212 or +56 (2) 687 2400. '
            'If the phone number contains an extension, it is RECOMMENDED '
            'that the extension be represented using the RFC 3966 [RFC3966] '
            'extension syntax, for example, +1 (604) 555-1234;ext=5678.'
        ),
        required=False
    )

    phone_number_verified = ps.Bool(
        title=_('Id Phone Number Verified'),
        description=_(
            'True if the End-User\'s phone number has been verified; otherwise false. '
            'When this Claim Value is true, this means that the OP took affirmative '
            'steps to ensure that this phone number was controlled by the '
            'End-User at the time the verification was performed. The means by which a '
            'phone number is verified is context-specific, and dependent upon the '
            'trust framework or contractual agreements within which the parties are operating. '
            'When true, the phone_number Claim MUST be in E.164 format and any extensions MUST '
            'be represented in RFC 3966 format'
        )
    )

    address = ps.JSONField(
        title=_('Address'),
        description=_(
            'End-User\'s preferred postal address. '
            'The value of the address member is a JSON [RFC4627] structure containing '
            'some or all of the members defined in Section 5.1.1.'
        ),
        required=False
    )
    updated_at = ps.Datetime(
        title=_('last update time'),
        description=_(
            'number Time the End-User\'s information was last updated. '
            'Its value is a JSON number representing the number of seconds '
            'from 1970-01-01T0:0:0Z as measured in UTC until the date/time.'
        ),
        required=False
    )


@provider(IFormFieldProvider)
class IOidConnectClaims(IProvideOidConnectClaims):
    """Add password fields"""

    # Putting this in a separate fieldset for the moment:
    model.fieldset(
        'claims',
        label=_(u"OpenID Connect Claims"),
        fields=['phone_number', 'address']
    )

    directives.omitted(
        'sub',
        'name',
        'given_name',
        'family_name',
        'preferred_username',
        'email_verified',
        'phone_number_verified',
        'updated_at'
    )


@implementer(IProvideOidConnectClaims)
@adapter(IOidConnectUser)
class OidConnectClaimsProvider(object):

    def __init__(self, context):
        """context = instance of MembraneUser content type"""
        self.context = context

    @property
    def sub(self):
        """ """
        return IMembraneUserObject(self.context).getUserId()

    @sub.setter
    def sub(self, value):
        # When editing, the password field is empty in the browser; do
        # not do anything then.
        raise ValueError(
            _('Assigning value for sub is not allowed, it should derive from ID')
        )

    @property
    def preferred_username(self):
        """ """
        return self.context.preferred_username or \
            IMembraneUserObject(self.context).getUserName()

    @preferred_username.setter
    def preferred_username(self, value):
        """ """
        self.context.preferred_username = value

    @property
    def middle_name(self):
        """ """
        return self.context.middle_name

    @middle_name.setter
    def middle_name(self, value):
        """ """
        self.context.middle_name = value

    @property
    def name(self):
        return self.context.name or \
            IMembraneUserObject(self.context).get_full_name()

    @name.setter
    def name(self, value):
        """ """
        self.context.name = value

    @property
    def given_name(self):
        """ """
        return self.context.given_name or \
            self.context.first_name

    @given_name.setter
    def given_name(self, value):
        """ """
        self.context.given_name = value

    @property
    def family_name(self):
        """ """
        return self.context.family_name or \
            self.context.last_name

    @family_name.setter
    def family_name(self, value):
        """ """
        self.context.family_name = value

    @property
    def nickname(self):
        """ """
        return self.context.nickname

    @nickname.setter
    def nickname(self, value):
        """ """
        self.context.nickname = value

    @property
    def profile(self):
        """ """
        return self.context.profile

    @profile.setter
    def profile(self, value):
        """ """
        self.context.profile = value

    @property
    def picture(self):
        """ """
        return self.context.picture

    @picture.setter
    def picture(self, value):
        """ """
        self.context.picture = value

    @property
    def website(self):
        return self.context.website

    @website.setter
    def website(self, value):
        """ """
        self.context.website = value

    @property
    def email_verified(self):
        return self.context.email_verified

    @email_verified.setter
    def email_verified(self, value):
        """ """
        self.context.email_verified = value

    @property
    def gender(self):
        """ """
        self.context.gender

    @gender.setter
    def gender(self, value):
        """ """
        self.context.gender = value

    @property
    def birthdate(self):
        """ """
        return self.context.birthdate

    @birthdate.setter
    def birthdate(self, value):
        """ """
        self.context.birthdate = value

    @property
    def zoneinfo(self):
        """ """
        return self.context.zoneinfo

    @zoneinfo.setter
    def zoneinfo(self, value):
        """ """
        self.context.zoneinfo = value

    @property
    def locale(self):
        """ """
        return self.context.locale

    @locale.setter
    def locale(self, value):
        """ """
        self.context.locale = value

    @property
    def phone_number(self):
        """ """
        return self.context.phone_number

    @phone_number.setter
    def phone_number(self, value):
        """ """
        self.context.phone_number = value

    @property
    def phone_number_verified(self):
        """ """
        return self.context.phone_number_verified

    @phone_number_verified.setter
    def phone_number_verified(self, value):
        self.context.phone_number_verified = value

    @property
    def address(self):
        """ """
        return self.context.address

    @address.setter
    def address(self, value):
        """ """
        self.context.address = value

    @property
    def updated_at(self):
        """ """
        return self.context.updated_at or \
            self.context.modified

    @updated_at.setter
    def updated_at(self, value):
        """ """
        self.context.updated_at = value


@implementer(IMembraneUserObject)
@adapter(IOidConnectUser)
class OidConnectUser(object):
    """ """

    def __init__(self, context):
        """ """
        self.context = context

    def getUserId(self):
        """ """
        return IMembraneUser(self.context).getUserId()

    def getUserName(self):
        """ """
        return IMembraneUser(self.context).getUserName()
