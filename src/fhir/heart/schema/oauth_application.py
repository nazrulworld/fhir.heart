# -*- coding: utf-8 -*-
# @Date    : 2017-10-05 10:03:35
# @Author  : Md Nazrul Islam (email2nazrul@gmail.com)
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from fhir.heart.i18n import _
from plone.supermodel import model
from zope import schema as zs


__author__ = 'Md Nazrul Islam (email2nazrul@gmail.com)'


class IOAuth2Application(model.Schema):
    """Meta Info:
    http://openid.net/specs/openid-connect-registration-1_0.html#ClientMetadata"""

    client_name = zs.TextLine(
        title=_('Application Name'),
        description=_(
            'Name of the Client to be presented to the End-User. '
            'If desired, representation of this Claim in different '
            'languages and scripts is represented as described in Section 2.1.'
        ),
        required=True
    )
    redirect_uris = zs.List(
        title=_('Redirect URIs'),
        description=_(
            'Array of Redirection URI values used by the Client. '
            'One of these registered Redirection URI values MUST '
            'exactly match the redirect_uri parameter value used in each '
            'Authorization Request, with the matching performed as described in '
            'Section 6.2.1 of [RFC3986] (Simple String Comparison).'
        ),
        value_type=zs.URI(),
        required=True
    )
    response_types = zs.List(
        title=_('Response Type'),
        description=_(
            'JSON array containing a list of the OAuth 2.0 response_type values '
            'that the Client is declaring that it will restrict itself to using. '
            'If omitted, the default is that the Client will use only the code Response Type.'
        ),
        value_type=zs.Choice(vocabulary='oauth2_app_response_type_options')
    )

    grant_types = zs.List(
        title=_('Grant Types'),
        description=_(
            'JSON array containing a list of the OAuth 2.0 Grant Types that the '
            'Client is declaring that it will restrict itself to using. '
        ),
        value_type=zs.Choice(vocabulary='oauth2_app_grant_type_options'),
        required=False

    )

    application_type = zs.Choice(
        title=_('Application Type'),
        description=_(
            'Kind of the application. The default, if omitted, is web. '
            'The defined values are native or web. Web Clients using the OAuth Implicit '
            'Grant Type MUST only register URLs using the https scheme as redirect_uris; '
            'they MUST NOT use localhost as the hostname. Native Clients MUST only register '
            'redirect_uris using custom URI schemes or URLs using the http: scheme with '
            'localhost as the hostname. Authorization Servers MAY place additional constraints '
            'on Native Clients. Authorization Servers MAY reject Redirection URI values using '
            'the http scheme, other than the localhost case for Native Clients. '
            'The Authorization Server MUST verify that all the registered redirect_uris '
            'conform to these constraints. This prevents sharing a Client ID across different '
            'types of Clients'
        ),
        vocabulary='oauth2_app_type_options',
        default='web'
    )

    contacts = zs.List(
        title=_('Contact E-mails'),
        description=_(
            'Array of e-mail addresses of people responsible for this Client. '
            'This might be used by some providers to enable a Web user '
            'interface to modify the Client information.'
        ),
        value_type=zs.TextLine(),
        required=False
    )

    logo_uri = zs.URI(
        title=_('Logo URI'),
        description=_(
            'URL that references a logo for the Client application. '
            'If present, the server SHOULD display this image to the '
            'End-User during approval. The value of this field MUST point '
            'to a valid image file. If desired, representation of this '
            'Claim in different languages and scripts is represented as '
            'described in Section 2.1.'
        ),
        required=False
    )

    client_uri = zs.URI(
        title=_('Application URI'),
        description=_(
            'URL of the home page of the Client. The value of this field MUST point to a '
            'valid Web page. If present, the server SHOULD display this URL to '
            'the End-User in a followable fashion. If desired, representation of this '
            'Claim in different languages and scripts is represented as described in Section 2.1.'
        ),
        required=False
    )

    policy_uri = zs.URI(
        title=_('Policy URI'),
        description=_(
            'URL that the Relying Party Client provides to the End-User to '
            'read about the how the profile data will be used. '
            'The value of this field MUST point to a valid web page. '
            'The OpenID Provider SHOULD display this URL to the End-User if it is given. '
            'If desired, representation of this Claim in different languages and scripts '
            'is represented as described in Section 2.1.'
        ),
        required=False
    )

    tos_uri = zs.URI(
        title=_('Terms of service URI'),
        description=_(
            'URL that the Relying Party Client provides to the End-User to read about '
            'the Relying Party\'s terms of service. The value of this field MUST point '
            'to a valid web page. The OpenID Provider SHOULD display this URL to '
            'the End-User if it is given. If desired, representation of this Claim '
            'in different languages and scripts is represented as described in Section 2.1.'
        ),
        required=False
    )

    jwks_uri = zs.URI(
        title=_('JWKS URI'),
        description=_(
            'URL for the Client\'s JSON Web Key Set [JWK] document. If the Client signs requests '
            'to the Server, it contains the signing key(s) the Server uses to validate signatures '
            'from the Client. The JWK Set MAY also contain the Client\'s encryption keys(s), '
            'which are used by the Server to encrypt responses to the Client. When both signing '
            'and encryption keys are made available, a use (Key Use) parameter value is '
            'REQUIRED for all keys in the referenced JWK Set to indicate each key\'s intended usage. '
            'Although some algorithms allow the same key to be used for both signatures and '
            'encryption, doing so is NOT RECOMMENDED, as it is less secure. '
            'The JWK x5c parameter MAY be used to provide X.509 representations of keys provided. '
            'When used, the bare key values MUST still be present and MUST match those in '
            'the certificate.'
        ),
        required=False
    )
    # jwks: https://tools.ietf.org/html/draft-ietf-jose-json-web-key-41#section-3
    jwks = zs.Dict(
        title=_('JSON Web Key Set'),
        description=_(
            'JSON Object. JSON Web Key Set [JWK] document, passed by value. '
            'The semantics of the jwks parameter are the same as the jwks_uri parameter, '
            'other than that the JWK Set is passed by value, rather than by reference. '
            'This parameter is intended only to be used by Clients that, for some reason, '
            'are unable to use the jwks_uri parameter, for instance, by native applications '
            'that might not have a location to host the contents of the JWK Set. '
            'If a Client can use jwks_uri, it MUST NOT use jwks. One significant downside of '
            'jwks is that it does not enable key rotation (which jwks_uri does, as described '
            'in Section 10 of OpenID Connect Core 1.0 [OpenID.Core]). '
            'The jwks_uri and jwks parameters MUST NOT be used together.'
        ),
        required=False
    )

    sector_identifier_uri = zs.URI(
        title=_('Sector Identifier URI'),
        description=_(
            'URL using the https scheme to be used in calculating Pseudonymous Identifiers '
            'by the OP. The URL references a file with a single JSON array of redirect_uri values. '
            'Please see Section 5. Providers that use pairwise sub (subject) values SHOULD '
            'utilize the sector_identifier_uri value provided in the Subject Identifier calculation '
            'for pairwise identifiers.')
    )

    subject_type = zs.Choice(
        title=_('Subject Type'),
        description=_(
            'subject_type requested for responses to this Client. '
            'The subject_types_supported Discovery parameter contains a list of '
            'the supported subject_type values for this server. Valid types include '
            'pairwise and public.'
        ),
        values=('pairwise', 'public'),
        required=False
    )

    id_token_signed_response_alg = zs.Choice(
        title=_('ID Token Response algorithms'),
        description=_(
            'JWS alg algorithm [JWA] REQUIRED for signing the ID Token issued to this Client.'
            'The value none MUST NOT be used as the ID Token alg value unless the '
            'Client uses only Response Types that return no ID Token from the '
            'Authorization Endpoint (such as when only using the Authorization Code Flow). '
            'The default, if omitted, is RS256. The public key for validating the '
            'signature is provided by retrieving the JWK Set referenced by the '
            'jwks_uri element from OpenID Connect Discovery 1.0 [OpenID.Discovery].'
        ),
        vocabulary='oauth2_app_jwt_algs_options',
        required=False
    )

    id_token_encrypted_response_alg = zs.Choice(
        title=_('ID Token encrypted response algorithm'),
        description=_(
            'JWE alg algorithm [JWA] REQUIRED for encrypting the ID Token issued to this Client. '
            'If this is requested, the response will be signed then encrypted, with the result '
            'being a Nested JWT, as defined in [JWT]. The default, if omitted, is that no '
            'encryption is performed.'
        ),
        vocabulary='oauth2_app_jwt_algs_options',
        required=False
    )

    id_token_encrypted_response_enc = zs.Choice(
        title=_('ID Token encrypted response enc'),
        description=_(
            'JWE enc algorithm [JWA] REQUIRED for encrypting the ID Token issued to this Client. '
            'If id_token_encrypted_response_alg is specified, the default for this value is '
            'A128CBC-HS256. When id_token_encrypted_response_enc is included, '
            'id_token_encrypted_response_alg MUST also be provided.'
        ),
        vocabulary='oauth2_app_jwt_enc_options',
        required=False
    )

    userinfo_signed_response_alg = zs.Choice(
        title=_('userinfo_signed_response_alg'),
        description=_(
            'JWS alg algorithm [JWA] REQUIRED for signing UserInfo Responses. '
            'If this is specified, the response will be JWT [JWT] serialized, and signed using JWS. '
            'The default, if omitted, is for the UserInfo Response to return the Claims as a '
            'UTF-8 encoded JSON object using the application/json content-type.'
        ),
        vocabulary='oauth2_app_jwt_algs_options',
        required=False
    )

    userinfo_encrypted_response_alg = zs.Choice(
        title=_('userinfo encrypted response algorithm'),
        description=_(
            'JWE [JWE] alg algorithm [JWA] REQUIRED for encrypting UserInfo '
            'Responses. If both signing and encryption are requested, the response will '
            'be signed then encrypted, with the result being a Nested JWT, as defined in '
            '[JWT]. The default, if omitted, is that no encryption is performed.'
        ),
        vocabulary='oauth2_app_jwt_algs_options',
        required=False
    )

    request_object_signing_alg = zs.Choice(
        title=_('request_object_signing_alg'),
        description=_(
            'JWS [JWS] alg algorithm [JWA] that MUST be used for signing Request Objects sent '
            'to the OP. All Request Objects from this Client MUST be rejected, '
            'if not signed with this algorithm. Request Objects are described in Section 6.1 of '
            'OpenID Connect Core 1.0 [OpenID.Core]. This algorithm MUST be used both when the '
            'Request Object is passed by value (using the request parameter) and when '
            'it is passed by reference (using the request_uri parameter). '
            'Servers SHOULD support RS256. The value none MAY be used. The default, if omitted, '
            'is that any algorithm supported by the OP and the RP MAY be used.'),
        vocabulary='oauth2_app_jwt_algs_options',
        required=False
    )

    request_object_encryption_alg = zs.Choice(
        title=_('request_object_encryption_alg'),
        description=_(
            'JWE [JWE] alg algorithm [JWA] the RP is declaring that it may use for '
            'encrypting Request Objects sent to the OP. This parameter SHOULD be included when '
            'symmetric encryption will be used, since this signals to the OP that a client_secret '
            'value needs to be returned from which the symmetric key will be derived, '
            'that might not otherwise be returned. The RP MAY still use other supported encryption '
            'algorithms or send unencrypted Request Objects, even when this parameter is present. '
            'If both signing and encryption are requested, the Request Object will be signed then '
            'encrypted, with the result being a Nested JWT, as defined in [JWT]. '
            'The default, if omitted, is that the RP is not declaring whether it might encrypt any '
            'Request Objects.'
        ),
        vocabulary='oauth2_app_req_obj_algs_options',
        required=False
    )
    request_object_encryption_enc = zs.Choice(
        title=_('request_object_encryption_enc'),
        description=_(
            'WE enc algorithm [JWA] the RP is declaring that it may use for encrypting '
            'Request Objects sent to the OP. If request_object_encryption_alg is specified, '
            'the default for this value is A128CBC-HS256. When request_object_encryption_enc '
            'is included, request_object_encryption_alg MUST also be provided.'
        ),
        vocabulary='oauth2_app_jwt_enc_options',
        required=False
    )

    token_endpoint_auth_method = zs.Choice(
        title=_('token_endpoint_auth_method'),
        description=_(
            'Requested Client Authentication method for the Token Endpoint. '
            'The options are client_secret_post, client_secret_basic, client_secret_jwt, '
            'private_key_jwt, and none, as described in Section 9 of '
            'OpenID Connect Core 1.0 [OpenID.Core]. Other authentication methods MAY be '
            'defined by extensions. If omitted, the default is client_secret_basic -- '
            'the HTTP Basic Authentication Scheme specified in Section 2.3.1 of '
            'OAuth 2.0 [RFC6749].'
        ),
        vocabulary='oauth2_app_token_endpoint_auth_method_options',
        required=False
    )
    token_endpoint_auth_signing_alg = zs.Choice(
        title=_('token_endpoint_auth_signing_alg'),
        description=_(
            'JWS [JWS] alg algorithm [JWA] that MUST be used for signing the JWT [JWT] '
            'used to authenticate the Client at the Token Endpoint for the private_key_jwt '
            'and client_secret_jwt authentication methods. All Token Requests using these '
            'authentication methods from this Client MUST be rejected, if the JWT is not '
            'signed with this algorithm. Servers SHOULD support RS256. '
            'The value none MUST NOT be used. The default, if omitted, is that any '
            'algorithm supported by the OP and the RP MAY be used.'
        ),
        vocabulary='oauth2_app_jwt_algs_options',
        required=False
    )

    default_max_age = zs.Decimal(
        title=_('Default Maximum Age'),
        description=_(
            'Default Maximum Authentication Age. Specifies that the End-User MUST be '
            'actively authenticated if the End-User was authenticated longer ago than '
            'the specified number of seconds. The max_age request parameter overrides this '
            'default value. If omitted, no default Maximum Authentication Age is specified.'
        ),
        required=False
    )

    require_auth_time = zs.Bool(
        title=_('Is require auth time'),
        description=_(
            'Boolean value specifying whether the auth_time Claim in the ID Token is REQUIRED. '
            'It is REQUIRED when the value is true. (If this is false, the auth_time Claim '
            'can still be dynamically requested as an individual Claim for the ID Token using '
            'the claims request parameter described in Section 5.5.1 of OpenID Connect Core 1.0 '
            '[OpenID.Core].) If omitted, the default value is false.'
        ),
        required=False
    )
    default_acr_values = zs.TextLine(
        title=_('default_acr_values'),
        description=_(
            'Default requested Authentication Context Class Reference values. '
            'Array of strings that specifies the default acr values that the OP '
            'is being requested to use for processing requests from this Client, '
            'with the values appearing in order of preference. The Authentication Context '
            'Class satisfied by the authentication performed is returned as the acr '
            'Claim Value in the issued ID Token. The acr Claim is requested as a Voluntary '
            'Claim by this parameter. The acr_values_supported discovery element contains a '
            'list of the supported acr values supported by this server. Values specified in '
            'the acr_values request parameter or an individual acr Claim request override '
            'these default values.'
        ),
        required=False
    )

    initiate_login_uri = zs.URI(
        title=_('initiate_login_uri'),
        description=_(
            'URI using the https scheme that a third party can use to initiate a login by the RP, '
            'as specified in Section 4 of OpenID Connect Core 1.0 [OpenID.Core]. '
            'The URI MUST accept requests via both GET and POST. The Client MUST understand '
            'the login_hint and iss parameters and SHOULD support the target_link_uri parameter.'
        ),
        required=False
    )
    request_uris = zs.List(
        title=_('request_uris'),
        description=_(
            'Array of request_uri values that are pre-registered by the RP for use at the OP. '
            'Servers MAY cache the contents of the files referenced by these URIs and not '
            'retrieve them at the time they are used in a request. OPs can require that '
            'request_uri values used be pre-registered with the require_request_uri_registration '
            'discovery parameter. If the contents of the request file could ever change, these URI '
            'values SHOULD include the base64url encoded SHA-256 hash value of the file contents '
            'referenced by the URI as the value of the URI fragment. If the fragment value used for '
            'a URI changes, that signals the server that its cached value for that URI with the old '
            'fragment value is no longer valid.'
        ),
        value_type=zs.URI(),
        required=False
    )
    # http://openid.net/specs/openid-connect-session-1_0.html#OPMetadata
    post_logout_redirect_uri = zs.List(
        title=_('post_logout_redirect_uri'),
        description=_(
            'Array of URLs supplied by the RP to which it MAY request that the End-User\'s '
            'User Agent be redirected using the post_logout_redirect_uri parameter after a '
            'logout has been performed.'
        ),
        value_type=zs.URI(),
        required=False
    )
    # https://www.rfc-editor.org/rfc/rfc7591.txt
    scope = zs.TextLine(
        title=_('Scope'),
        description=_(
            'String containing a space-separated list of scope values (as'
            'described in Section 3.3 of OAuth 2.0 [RFC6749]) that the client'
            'can use when requesting access tokens.  The semantics of values in'
            'this list are service specific.  If omitted, an authorization'
            'server MAY register a client with a default set of scopes.'
        ),
        required=False
    )
    software_id = zs.TextLine(
        title=_('Software ID'),
        description=_(
            'A unique identifier string (e.g., a Universally Unique Identifier'
            '(UUID)) assigned by the client developer or software publisher'
            'used by registration endpoints to identify the client software to'
            'be dynamically registered.'
        ),
        required=False
    )
    client_id = zs.TextLine(
        title=_('Client ID'),
        description=_(
            'OAuth 2.0 client identifier string.  It SHOULD NOT be'
            'currently valid for any other registered client, though an'
            'authorization server MAY issue the same client identifier to'
            'multiple instances of a registered client at its discretion.'
        ),
        required=True
    )
    client_secret = zs.TextLine(
        title=_('Client Secret'),
        description=_(
            'OAuth 2.0 client secret string.  If issued, this MUST'
            'be unique for each "client_id" and SHOULD be unique for multiple'
            'instances of a client using the same "client_id".  This value is'
            'used by confidential clients to authenticate to the token'
            'endpoint, as described in OAuth 2.0 [RFC6749], Section 2.3.1.'
        ),
        required=False
    )

    client_type = zs.Choice(
        title=_('Client Type'),
        description=_('Type clients, i.e public or secret'),
        vocabulary='oauth2_app_client_type_options',
        required=False
    )

    client_id_issued_at = zs.Datetime(
        title=_('Client ID Issued at'),
        description=_(
            'Time at which the client identifier was issued.  The'
            'time is represented as the number of seconds from'
            '1970-01-01T00:00:00Z as measured in UTC until the date/time of'
            'issuance.'
        )
    )

    client_secret_expires_at = zs.Datetime(
        title=_('Client Secret Expire at'),
        description=_(
            'REQUIRED if "client_secret" is issued.  Time at which the client'
            'secret will expire or 0 if it will not expire.  The time is'
            'represented as the number of seconds from 1970-01-01T00:00:00Z as'
            'measured in UTC until the date/time of expiration.'
        ),
        required=False
    )

    domain = zs.TextLine(
        title=_('FQ Domain Name'),
        description=_(''),
        required=False
    )
