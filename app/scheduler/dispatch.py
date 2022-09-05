import httpx

def make_call(verb, url):
    print(f" >> start: {verb} {url}")

    if verb == 'GET':
        httpx.get(url)
    if verb == 'POST':
        httpx.post(url)

    print(f" << finished call: {verb} {url}")

async def run():
    print("asdasd")
    # retrieve all scheduled hooks (ticks without effectively ran at)
    # update the effectivelly ran for each
    # make the actual http call
    # create a runs table record
    # create a hits record with the response of the http call



