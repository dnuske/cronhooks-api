from app.db.conn import engine
from sqlalchemy import text

from app.utils import HookDatatype


async def add_run(hook_id, next_scheduled_at):
    async with engine.connect() as conn:
        q = text('insert into runs(hook_id, scheduled_at) values(:hook_id, :scheduled_at);')
        result = await conn.execute(q, {"hook_id": hook_id, "scheduled_at": next_scheduled_at})
        await conn.commit()
        return True

async def find_previous_runs(hook_id):
    async with engine.connect() as conn:
        result = await conn.execute(text("""select scheduled_at from runs where hook_id = :hook_id;"""),
                                    {"hook_id": hook_id})
        await conn.commit()
        res = result.fetchone()
        if res:
            res.scheduled_at

async def find_not_scheduled_hooks():
    async with engine.connect() as conn:
        result = await conn.execute(text("""select hooks.id as id, created_at, updated_at, method, url, body, cron, headers, last_hit, user_id
            from hooks
            left join runs
            on hooks.id = runs.hook_id
            where runs.scheduled_at is null
            or (runs.scheduled_at is null and runs.effectively_ran_at is not null)
            """))
        await conn.commit()
        return result.fetchall()

async def find_pending_runs():
    async with engine.connect() as conn:
        result = await conn.execute(text("""select hooks.*, runs.id as run_id
            from hooks, runs
            where hooks.id = runs.hook_id
            and runs.effectively_ran_at is  null
            and hit_id is null
            and scheduled_at < now();
            """))
        await conn.commit()
        return result.fetchall()


async def update_run_effectively_run(run_id, effectively_ran_at):
    async with engine.connect() as conn:
        r = await conn.execute(text("update runs set effectively_ran_at=:effectively_ran_at where run_id = :run_id"), {"run_id": run_id, "effectively_ran_at": effectively_ran_at})
        await conn.commit()
        return True


async def add_hit(hook_id, res_status, res_data, started_at, finished_at):
    async with engine.connect() as conn:
        r = await conn.execute(text("insert into hits(hook_id, response_status, response_data, started_at, finished_at) values(:hook_id, :response_status, :response_data, :started_at, :finished_at);"),
                               {"hook_id": hook_id, "response_status": res_status, "response_data": res_data, "started_at": started_at, "finished_at": finished_at})
        await conn.commit()
        return True

