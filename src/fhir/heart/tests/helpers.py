# -*- coding: utf-8 -*-
# @Date    : 2018-01-29 17:42:51
# @Author  : Md Nazrul Islam (email2nazrul@gmail.com)
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from fhir.heart.compat import pathlib

import os


__author__ = 'Md Nazrul Islam (email2nazrul@gmail.com)'


FIXTURE_DIRECTORY = pathlib.Path(os.path.dirname(os.path.abspath(__file__))) / 'fixtures'
STATIC_FHIR_DIRECTORY = FIXTURE_DIRECTORY / 'FHIR'