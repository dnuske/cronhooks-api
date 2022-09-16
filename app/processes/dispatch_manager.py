import httpx
from datetime import datetime

from app.db import process


def make_call(verb, url):
    # fetch only up to 10kb
    # timeout in 60 seconds
    print(f" >> start: {verb} {url}")

    if verb == 'GET':
        return httpx.get(url)
    if verb == 'POST':
        return httpx.post(url)

    print(f" << finished call: {verb} {url}")

async def run():
    print("asdasd")
    # retrieve all scheduled hooks (ticks without effectively ran at)
    hooks = await process.find_pending_runs()
    # update the effectivelly ran for each
    for hook in hooks:
        try:

            started_at = datetime.now()
            # TODO: deal with time zones eventually
            print('----', hook.run_id, started_at)
            await process.update_run_effectively_run(hook.run_id, started_at)
            # make the actual http call
            response_text = ''
            try:
                print(" +++++++++++++ make call", hook.method, hook.url)
                res = make_call(hook.method, hook.url)
                response_text = res.text
            except Exception as e:
                response_text = str(e)
                print(e)

            await process.update_hook_last_hit(hook.id, started_at)
            print("update_hook_last_hit", hook.id, started_at)

            print(" ++++ response ", res.text, res.status_code)
            finished_at = datetime.now()



            # create a hits record with the response of the http call
            await process.add_hit(hook.id, res.status_code, response_text, started_at, finished_at)

        except Exception as e:
            response_text = str(e)
            print(e)









