import os
import re
from random import choice

from aiohttp import web

from ali_partner.logger import logger, exception_message

random_links = ['https://blog.yottos.com/rabota-v-yottos-2/'
                'https://blog.yottos.com/reklamnye-programmy/'
                'https://blog.yottos.com/stil-yottos/logotipy/'
                'https://blog.yottos.com/kovriki/']


class ApiView(web.View):
    async def get_data(self):
        static_path = os.path.join(self.request.app['config']['dir_path'], 'static')
        tail = self.request.match_info['tail']
        ip = '127.0.0.1'
        ip_regex = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
        headers = self.request.headers

        x_real_ip = headers.get('X-Real-IP', headers.get('X-Forwarded-For', ''))
        x_real_ip_check = ip_regex.match(x_real_ip)
        if x_real_ip_check:
            x_real_ip = x_real_ip_check.group()
        else:
            x_real_ip = None

        if x_real_ip is not None:
            ip = x_real_ip
        else:
            try:
                peername = self.request.transport.get_extra_info('peername')
                if peername is not None and isinstance(peername, tuple):
                    ip, _ = peername
            except Exception as ex:
                logger.error(exception_message(exc=str(ex), request=str(self.request._message)))

        data = {
            'ip': ip
        }
        if self.request.not_uniq or self.request.fail_referer:
            file_path = os.path.join(static_path, tail)
            file_exists = os.path.isfile(file_path)
            if not file_exists:
                file_path = os.path.join(static_path, 'index.html')
            if self.request.user_cookie % 4 != 0:
                return web.FileResponse(path=file_path)
            return web.HTTPFound(choice(random_links))
        else:
            return web.HTTPFound('https://blog.yottos.com/')

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
