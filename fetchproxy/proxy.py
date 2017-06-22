# -*- coding: utf-8 -*-

import concurrent.futures
import json
from .resolver import resolve, TIMEOUT


class Proxy(object):
    def __init__(self, address: str, port: int, anonymity: str, typ: str):
        self.address = address
        self.port = port
        self.region = ''
        self.anonymity = anonymity
        self.type = typ
        self.resp_time = 0.0

    def __lt__(self, other):
        if not isinstance(other, Proxy):
            raise NotImplementedError
        return self.resp_time < other.resp_time

    def __repr__(self):
        return f'[{self.type}, {self.address}:{self.port}] - {self.anonymity} {self.region}'

    def ping(self):
        self.region, self.resp_time = resolve(self.address, self.port, self.type)

    def json(self):
        return json.dumps(
            {'address': self.address, 'port': self.port, 'region': self.region,
             'anonymity': self.anonymity, 'type': self.type,
             'resp_time': self.resp_time}
        )


class ProxyPlugin(object):
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.proxies = []

    def remove_dead_proxies(self):
        for proxy in self.proxies[:]:
            if proxy.resp_time == TIMEOUT:
                self.proxies.remove(proxy)

    def fetches(self):
        self.fetch_proxies()
        self.ping_proxies()

    def fetch_proxies(self):
        # Fetch proxy list from address
        return self.proxies

    def ping_proxies(self):
        # Ping proxy list
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            for proxy in self.proxies:
                executor.submit(proxy.ping)
        self.remove_dead_proxies()
