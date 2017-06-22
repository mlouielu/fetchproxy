# -*- coding: utf-8 -*-

import concurrent.futures
from .plugins import plugins


if __name__ == '__main__':
    proxies = [p() for p in plugins]
    with concurrent.futures.ThreadPoolExecutor(10) as executor:
        for proxy in proxies:
            executor.submit(proxy.fetches)

    import pdb
    pdb.set_trace()
