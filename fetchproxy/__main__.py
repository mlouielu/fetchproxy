# -*- coding: utf-8 -*-

import concurrent.futures
from .plugins import plugins


if __name__ == '__main__':
    sites = [p() for p in plugins]
    with concurrent.futures.ThreadPoolExecutor(10) as executor:
        for proxy in sites:
            executor.submit(proxy.fetches)

    for proxies in sites:
        for proxy in proxies.proxies:
            print(proxy.json())
