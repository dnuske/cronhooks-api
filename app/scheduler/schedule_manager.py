from croniter import croniter
from datetime import datetime

from app.db import db


def determine_next_schedule(previous_tick, hook_cron):
  base = previous_tick
  iter = croniter(hook_cron, base)  # every 5 minutes
  return iter.get_next(datetime)


async def run():
  print(0)
  not_scheduled_hooks = await db.find_not_scheduled_hooks()
  print(1, not_scheduled_hooks)
  for not_scheduled_hook in not_scheduled_hooks:
    print(2, not_scheduled_hook.id)
    previous_tick = await db.find_previous_tick(not_scheduled_hook.id)
    print(3, previous_tick)

    if not previous_tick:
      print(4)
      previous_tick = datetime.now()
    print(5, previous_tick)
    next_tick = determine_next_schedule(previous_tick, not_scheduled_hook.cron)
    print(6, next_tick)
    await db.add_scheduler_tick(not_scheduled_hook.id, next_tick)
    print(7)


