# -*- coding: utf-8 -*-

import requests
from lxml import etree
from ..proxy import Proxy, ProxyPlugin


class SSLProxies(ProxyPlugin):
    def __init__(self):
        self.name = 'sslproxies.org'
        self.address = 'https://www.sslproxies.org'

    def fetch_proxies(self):
        resp = requests.get(self.address)
        root = etree.HTML(resp.text)

        self.proxies = []
        for proxy in root.xpath('//tbody/tr'):
            addr, port, _, _, anonymity, _, https, _ = list(proxy.itertext())
            typ = 'https' if https.startswith('yes') else 'http'
            self.proxies.append(Proxy(addr, port, anonymity, typ))

        return self.proxies
