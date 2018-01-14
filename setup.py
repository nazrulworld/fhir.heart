# -*- coding: utf-8 -*-
"""Installer for the fhir.heart package."""

from setuptools import find_packages
from setuptools import setup

import sys


PY2 = sys.version_info[0] == 2
PY34 = sys.version_info[0:2] >= (3, 4)

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
    open('SPECS.rst').read(),
    open('LINKS.rst').read(),
])

install_requires = [
    'six',
    'plone.api',
    'plone.restapi',
    'plone.app.fhirfield',
    'plone.app.jsonfield',
    'plone.formwidget.contenttree',
    'plone.namedfile',
    'plone.formwidget.namedfile',
    'setuptools',
    'Products.GenericSetup>=1.8.2',
    'z3c.jbot',
    'dexterity.membrane>=2.0',
    'Products.membrane>=3.0.2',
    'oauthlib',
    'python-social-auth',
    'certifi',
    'chardet',
    'cryptography',
    'oic',
    'pysaml2',
    'pyjwkest',
    'fhirclient',
    'collective.vdexvocabulary',
    'python-jose'
]

if PY2:
    install_requires.append('pathlib2')

setup(
    name='fhir.heart',
    version='1.0.0a2.dev0',
    description='Health Relationship Trust Profile (HEART) implementation for FHIR (Fast Healthcare Interoperability Resources) compliance '
    'for Healthcare System.',
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.0',
        'Framework :: Plone :: 5.1',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    ],
    keywords='Python Plone oauth2 fhir openid',
    author='Md Nazrul Islam',
    author_email='email2nazrul@gmail.com',
    url='https://pypi.python.org/pypi/fhir.heart',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['fhir'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
