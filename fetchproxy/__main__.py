# -*- coding: utf-8 -*-

from .plugins import usproxy


if __name__ == '__main__':
    p = usproxy.USProxy()
    p.fetch_proxies()
    p.ping_proxies()

    for proxy in p.proxies:
        print(proxy.json())
