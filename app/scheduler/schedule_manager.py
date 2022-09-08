from croniter import croniter
from datetime import datetime

from app.db import process


def determine_next_schedule(previous_run, hook_cron):
  base = previous_run
  iter = croniter(hook_cron, base)  # every 5 minutes
  return iter.get_next(datetime)


async def run():
  print(0)
  not_scheduled_hooks = await process.find_not_scheduled_hooks()
  print(1, not_scheduled_hooks)
  for not_scheduled_hook in not_scheduled_hooks:
    print(2, not_scheduled_hook.id)
    previous_run = await process.find_previous_runs(not_scheduled_hook.id)
    print(3, previous_run)

    if not previous_run:
      print(4)
      previous_run = datetime.now()
    print(5, previous_run)
    next_tick = determine_next_schedule(previous_run, not_scheduled_hook.cron)
    print(6, next_tick)
    await process.add_run(not_scheduled_hook.id, next_tick)
    print(7)


