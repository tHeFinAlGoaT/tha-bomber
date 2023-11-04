def get_proxies() -> list:
    with open("settings/proxies.txt") as f:
        proxies = f.read().splitlines()
    return proxies

if __name__ == "__main__":
    print(get_proxies())