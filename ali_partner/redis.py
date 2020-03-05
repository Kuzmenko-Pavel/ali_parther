import aioredis


async def init_redis(app):
    conf = app['config']['redis']
    app.redis_pool = await aioredis.create_redis_pool(
        conf['uri'],
        minsize=1, maxsize=5)


async def close_redis(app):
    app.redis_pool.close()
    await app.redis_pool.wait_closed()


async def stored(redis, data):
    time = 60 * 60 * 24 * 4
    account_id = data.get('account_id')
    ids = data.get('ids', [])
    if account_id and ids:
        pipe = redis.pipeline()
        for item in ids:
            try:
                key = '%s::%s' % (str(account_id).strip(), str(item).strip())
                key_exists = 'exists::%s' % str(account_id).strip()
                pipe.incr(key)
                pipe.set(key_exists, 1)
                pipe.expire(key, time)
                pipe.expire(key_exists, time)
            except Exception as e:
                print(e)
        await pipe.execute()
