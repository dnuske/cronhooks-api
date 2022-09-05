
from app.db.conn import engine
from sqlalchemy import text

from app.utils import HookDatatype


async def get_all_hooks(user_id: str):
    async with engine.connect() as conn:
        result = await conn.execute(text("""select id, created_at, updated_at, method, url, body, cron, headers, last_hit, user_id
                                         from hooks where user_id = :user_id;"""), {"user_id": user_id})
        await conn.commit()
        return result.fetchall()


async def create_hook(hook: HookDatatype, user_id: str):
    async with engine.connect() as conn:
        q = text('insert into hooks(method, url, body, cron, headers, user_id) values(:method, :url, :body, :cron, :headers, :user_id);')
        result = await conn.execute(q, {"method": hook.method, "url": hook.url, "body": hook.body, "cron": hook.cron,
            "headers": hook.headers, "user_id": user_id})
        await conn.commit()
        return True


async def get_hook(_id: str):
    async with engine.connect() as conn:
        result = await conn.execute(text('''select id, created_at, updated_at, method, url, body, cron, headers, last_hit, user_id 
            from hooks
            where id = :id;'''), {"id": _id})
        await conn.commit()
        return result.fetchone()


async def update_hook(hook: HookDatatype):
    async with engine.connect() as conn:
        q = text('''update hooks set method=:method, url=:url, body=:body, cron=:cron, headers=:headers
            where id=:id;''')
        result = await conn.execute(q, {"method": hook.method, "url": hook.url, "body": hook.body, "cron": hook.cron,
            "headers": hook.headers, "id": hook.id})
        await conn.commit()

        return True


async def delete_hook(id: str):
    async with engine.connect() as conn:
        q = text('''delete from hooks where id=:id;''')
        result = await conn.execute(q, {"id": id})
        await conn.commit()

        return True


async def get_all_hook_hits(hook_id: str):
    async with engine.connect() as conn:
        result = await conn.execute(text('select started_at, finished_at, hook_id, response_status, response_data from hits where hook_id=:hook_id;'), {"hook_id": hook_id})
        await conn.commit()
        return result.fetchall()


async def hook_belongs_to_user(hook_id: str, user_id: str):
    async with engine.connect() as conn:
        result = await conn.execute(text('''select exists(select 1 from hooks 
            where id = :hook_id 
            and user_id = :user_id;'''), {"hook_id": hook_id, "user_id": user_id})
        await conn.commit()
        return result.one().exists


async def add_scheduler_tick(hook_id, next_tick):
    async with engine.connect() as conn:
        q = text('insert into scheduler_ticks(hook_id, tick) values(:hook_id, :tick);')
        result = await conn.execute(q, {"hook_id": hook_id, "tick": next_tick})
        await conn.commit()
        return True


async def find_previous_tick(hook_id):
    async with engine.connect() as conn:
        result = await conn.execute(text("""select tick from scheduler_ticks where hook_id = :hook_id;"""),
                                    {"hook_id": hook_id})
        await conn.commit()
        res = result.fetchone()
        if res:
            res.tick


async def find_not_scheduled_hooks():
    async with engine.connect() as conn:
        result = await conn.execute(text("""select hooks.id as id, created_at, updated_at, method, url, body, cron, headers, last_hit, user_id
            from hooks
            left join scheduler_ticks
            on hooks.id = scheduler_ticks.hook_id
            where scheduler_ticks.tick is null
            or (scheduler_ticks.tick is null and scheduler_ticks.effectively_ran_at is not null)
            """))
        await conn.commit()
        return result.fetchall()


