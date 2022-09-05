import httpx

def make_call(verb, url):
    print(f" >> start: {verb} {url}")

    if verb == 'GET':
        httpx.get(url)
    if verb == 'POST':
        httpx.post(url)

    print(f" << finished call: {verb} {url}")

