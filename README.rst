.. contents::

collective.fhir.heart
=====================

The the Health Relationship Trust (`HEART`_) implementation of IAM(Identity Access Management), authentication and security system for FHIR compliance healthcare system, powered by `OAuth 2.0`_, `OpenID Connect 1.0`_, `Plone`_.


Features
--------

- `HEART profile for OAuth 2.0`_.
- `HEART profile for OpenID Connect`_.
- `HEART profile for User-Managed Access (UMA)`_.
- HEART profile for Fast Healthcare Interoperability Resources (FHIR) OAuth 2.0 scopes.
- HEART profile for FHIR UMA resource set types, scopes, and claims-gathering flows (referencing the previous specifications as appropriate).


Examples
--------

This add-on can be seen in action at the following sites:
- Is there a page on the internet where everybody can see the features?


Documentation
-------------

Full documentation for end users can be found in the "docs" folder, and is also available online at http://docs.plone.org/foo/bar


Translations
------------

This product has been translated into

- Klingon (thanks, K'Plai)


Installation
------------

Install collective.fhir.heart by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.fhir.heart


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.fhir.heart/issues
- Source Code: https://github.com/collective/collective.fhir.heart
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@example.com


License
-------

The project is licensed under the GPLv2.