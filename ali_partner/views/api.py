import os
from random import choice, randint

from aiohttp import web

from ali_partner.partners import partner_links
from ali_partner.logger import logger

gotbest_range = 1.0


class ApiView(web.View):
    async def get_data(self, processed=None):
        if processed is None:
            return web.Response(body='')

        if self.request.fail_referer:
            static_path = os.path.join(self.request.app['config']['dir_path'], 'static')
            tail = self.request.match_info['tail']
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
