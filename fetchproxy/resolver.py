# -*- coding: utf-8 -*-

import os
import time
import maxminddb
import requests

TIMEOUT = 5

_mmdb_reader = maxminddb.open_database(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'GeoLite2-Country.mmdb'))


def resolve(addr, port, typ):
    try:
        info = _mmdb_reader.get(addr)
    except (maxminddb.errors.InvalidDatabaseError, ValueError):
        return ('', TIMEOUT)

    st = time.time()
    try:
        requests.head('https://google.com',
                      proxies={typ: f'{typ}://{addr}:{port}'},
                      timeout=TIMEOUT)
    except Exception as e:
        return ('', TIMEOUT)

    return info['country']['names']['en'], time.time() - st
