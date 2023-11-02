def proxies() -> list:
    with open('settings/proxies.txt') as p:
        proxies = p.read().splitlines()

    return proxies