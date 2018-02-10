# _*_ coding: utf-8 _*_
import time


__author__ = 'Md Nazrul Islam<email2nazrul@gmail.com>'


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
