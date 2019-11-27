import os
from collections import defaultdict
from random import choice, randint

from aiohttp import web


partner_links = defaultdict(lambda: {
    'partner_link': 'https://goodsbuy.by/redirect/cpa/o/q1n4uuu8p128gfd7b9pdawtm587hl1x8/',
    'partner_offers': ['https://www.gearbest.com/robot-vacuum/pp_009977063488.html',
                       'https://www.gearbest.com/vacuum-cleaners/pp_009847295038.html',
                       'https://www.gearbest.com/robot-vacuum/pp_009816316347.html',
                       'https://www.gearbest.com/vacuum-cleaners/pp_3001678459986936.html']
})

partner_links[1] = {
    'partner_link': 'https://goodsbuy.by/redirect/cpa/o/q1n4uuu8p128gfd7b9pdawtm587hl1x8/',
    'partner_offers': ['https://www.gearbest.com/robot-vacuum/pp_009977063488.html',
                       'https://www.gearbest.com/vacuum-cleaners/pp_009847295038.html',
                       'https://www.gearbest.com/robot-vacuum/pp_009816316347.html',
                       'https://www.gearbest.com/vacuum-cleaners/pp_3001678459986936.html']
}

partner_links[2] = {
    'partner_link': 'https://gotbest.by/redirect/cpa/o/q1n46ogyxk60g19uufihszjsy8qtya5i/',
    'partner_offers': ['https://ru.aliexpress.com/item/33057687661.html',
                       'https://ru.aliexpress.com/item/32818280372.html',
                       'https://ru.aliexpress.com/item/32811529988.html',
                       'https://ru.aliexpress.com/item/33055454479.html']
}


class ApiView(web.View):
    async def get_data(self):
        rand_req_count = randint(5, 7)
        static_path = os.path.join(self.request.app['config']['dir_path'], 'static')
        tail = self.request.match_info['tail']
        partner = self.request.partner
        partner_link = partner_links[partner]['partner_link']
        partner_offers = partner_links[partner]['partner_offers']
        if self.request.fail_referer:
            file_path = os.path.join(static_path, tail)
            file_exists = os.path.isfile(file_path)
            if not file_exists:
                file_path = os.path.join(static_path, 'index.html')
            return web.FileResponse(path=file_path)
        else:
            if self.request.not_uniq:
                if self.request.request_count % rand_req_count != 0:
                    return web.Response(body='')
                return web.HTTPFound(choice(partner_offers))
            else:
                return web.HTTPFound(partner_link)

    async def get(self):
        return await self.get_data()

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
