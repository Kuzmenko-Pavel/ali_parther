import os
from random import choice, randint

from aiohttp import web

from ali_partner.partners import partner_links
from ali_partner.logger import logger

gotbest_range = 0.1


class ApiView(web.View):
    async def get_data(self, processed=None):
        fingeprint = self.request.fingeprint

        static = False
        with await self.request.app.redis_pool as conn:
            val = await conn.ttl(fingeprint)
            if val > 0:
                static = True

            await conn.set(fingeprint, 1, expire=60*30)

        tail = self.request.match_info['tail']
        if processed is None:
            return web.Response(body='')

        if len(tail) > 0:
            static = True
            logger.info('Static request %s or user-agent %s or ip %s on %s' % (
                self.request.referer, self.request.user_agent, self.request.ip, tail
            ))
        else:
            if self.request.fail_referer or self.request.bot or self.request.is_customer:
                fail = 'Fail Referer'
                if self.request.bot:
                    fail = 'Fail BOT'
                if self.request.is_customer:
                    fail = 'Fail Customer'
                static = True
                logger.info('%s %s or user-agent %s or ip %s' % (fail, self.request.referer,
                                                                 self.request.user_agent, self.request.ip))

        if static:
            static_path = os.path.join(self.request.app['config']['dir_path'], 'static')
            file_path = os.path.join(static_path, tail)
            file_exists = os.path.isfile(file_path)
            if not file_exists:
                file_path = os.path.join(static_path, 'index.html')
            return web.FileResponse(path=file_path)

        if self.request.ali_visited:
            return web.Response(body='')

        partner = choice(list(partner_links.keys()))
        partner_link = partner_links[partner]['partner_link']
        partner_offers = partner_links[partner]['partner_offers']
        count_gotbest = self.request.app.view_count['gotbest']
        count_aliexpress = self.request.app.view_count['aliexpress']
        if (count_gotbest + count_aliexpress) % 1000 == 0:
            logger.info(('gotbest %s aliexpress %s' % (count_gotbest, count_aliexpress)))

        if count_gotbest > ((count_gotbest + count_aliexpress) / 100.0) * gotbest_range:
                self.request.app.view_count['aliexpress'] += 1
                return web.HTTPFound(choice(partner_offers))
        else:
            if self.request.partner_visited:
                self.request.app.view_count['aliexpress'] += 1
                return web.HTTPFound(choice(partner_offers))
            else:
                self.request.app.view_count['gotbest'] += 1
                return web.HTTPFound(partner_link)

    async def get(self):
        return await self.get_data(True)

    async def post(self):
        return await self.get_data()

    async def put(self):
        return await self.get_data()

    async def head(self):
        return await self.get_data()

    async def delete(self):
        return await self.get_data()

    async def patch(self):
        return await self.get_data()

    async def options(self):
        return await self.get_data()
