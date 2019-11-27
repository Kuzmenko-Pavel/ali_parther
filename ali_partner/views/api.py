import os
from collections import defaultdict
from random import choice, randint

from aiohttp import web


partner_links = defaultdict(lambda: {
    'partner_link': 'https://blog.yottos.com/',
    'partner_offers': ['https://blog.yottos.com/rabota-v-yottos-2/',
                       'https://blog.yottos.com/reklamnye-programmy/',
                       'https://blog.yottos.com/stil-yottos/logotipy/',
                       'https://blog.yottos.com/kovriki/']
})

partner_links[1] = {
    'partner_link': 'https://blog.yottos.com/',
    'partner_offers': ['https://blog.yottos.com/rabota-v-yottos-2/',
                       'https://blog.yottos.com/reklamnye-programmy/',
                       'https://blog.yottos.com/stil-yottos/logotipy/',
                       'https://blog.yottos.com/kovriki/']
}

partner_links[2] = {
    'partner_link': 'https://www.google.com/',
    'partner_offers': ['https://www.google.com/adsense/start/#/?modal_active=none',
                       'https://www.google.com/intl/ru/gmail/about/#',
                       'https://www.google.com/intl/ru/drive/',
                       'https://www.youtube.com/?gl=UA&tab=w11']
}


class ApiView(web.View):
    async def get_data(self):
        rand_req_count = randint(5, 7)
        static_path = os.path.join(self.request.app['config']['dir_path'], 'static')
        tail = self.request.match_info['tail']
        parther = self.request.parther
        partner_link = partner_links[parther]['partner_link']
        partner_offers = partner_links[parther]['partner_offers']
        if self.request.fail_referer:
            file_path = os.path.join(static_path, tail)
            file_exists = os.path.isfile(file_path)
            if not file_exists:
                file_path = os.path.join(static_path, 'index.html')
            return web.FileResponse(path=file_path)
        else:
            if self.request.not_uniq:
                if self.request.user_cookie % rand_req_count != 0:
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
