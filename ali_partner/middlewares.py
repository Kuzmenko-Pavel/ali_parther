from datetime import datetime, timedelta
import re
from aiohttp import web, hdrs
from hashlib import md5
from random import randint

from ali_partner.logger import logger, exception_message
from ali_partner.user_agents import simple_parse
from ali_partner.customer_ips import ip_pattern


async def handle_404(request, response):
    return web.Response(text='')


async def handle_405(request, response):
    return web.Response(text='')


async def handle_500(request, response):
    return web.Response(text='')


def error_pages(overrides):
    async def middleware(app, handler):
        async def middleware_handler(request):
            try:
                response = await handler(request)
                override = overrides.get(response.status)
                if override is None:
                    return response
                else:
                    return await override(request, response)
            except web.HTTPException as ex:
                if ex.status != 404:
                    logger.error(exception_message(exc=str(ex), request=str(request._message)))
                override = overrides.get(ex.status)
                if override is None:
                    raise
                else:
                    return await override(request, ex)

        return middleware_handler

    return middleware


async def cookie_middleware(app, handler):
    async def middleware(request):

        request.ali_visited = False
        request.partner_visited = False

        partner_cookie_name = 'puc'
        ali_cookie_name = 'auc'

        partner_cookie = request.cookies.get(partner_cookie_name)

        ali_cookie = request.cookies.get(ali_cookie_name)

        if partner_cookie:
            request.partner_visited = True

        if ali_cookie:
            request.ali_visited = True

        response = await handler(request)

        if not request.partner_visited:
            hours = 12 * 3
            partner_expires = datetime.utcnow() + timedelta(hours=hours)
            partner_cookie_expires = partner_expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
            partner_cookie_max_age = 60 * 60 * hours

            response.set_cookie(partner_cookie_name, randint(1, 1000000000), path='',
                                expires=partner_cookie_expires, max_age=partner_cookie_max_age, secure=True)

        if not request.ali_visited:
            hours = 12
            ali_expires = datetime.utcnow() + timedelta(hours=hours)
            ali_cookie_expires = ali_expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
            ali_cookie_max_age = 60 * 60 * hours

            response.set_cookie(ali_cookie_name, randint(1, 1000000000), path='',
                                expires=ali_cookie_expires, max_age=ali_cookie_max_age, secure=True)

        return response

    return middleware


async def detect_bot_middleware(app, handler):
    async def middleware(request):
        headers = request.headers
        request.user_agent = headers.get(hdrs.USER_AGENT, '')
        request.bot = simple_parse(request.user_agent) == 'bt'
        response = await handler(request)
        return response

    return middleware


async def check_referer_middleware(app, handler):
    async def middleware(request):
        headers = request.headers
        request.referer = headers.get(hdrs.REFERER, '')
        if 'rg.yottos.com' in request.referer:
            request.fail_referer = False
        else:
            request.fail_referer = True
        response = await handler(request)
        return response

    return middleware


async def fingerprint_middleware(app, handler):
    async def middleware(request):
        ip = '127.0.0.1'
        ip_regex = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
        headers = request.headers
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
                peername = request.transport.get_extra_info('peername')
                if peername is not None and isinstance(peername, tuple):
                    ip, _ = peername
            except Exception as ex:
                logger.error(exception_message(exc=str(ex), request=str(request._message)))

        headers = request.headers
        d = headers.get(hdrs.ACCEPT, '').replace(' ', '')
        d += headers.get(hdrs.ACCEPT_LANGUAGE, '').replace(' ', '')
        d += headers.get(hdrs.USER_AGENT, '').replace(' ', '')
        d += headers.get(hdrs.ACCEPT_ENCODING, '').replace(' ', '')
        d += headers.get('X-SSL-CERT', '').replace(' ', '')
        d += ip
        print(d)
        request.fingeprint = md5(d.encode('utf-8')).hexdigest()
        response = await handler(request)
        return response

    return middleware


async def disable_cache_middleware(app, handler):
    async def middleware(request):
        expiry_time = datetime.utcnow()
        response = await handler(request)
        response.headers[hdrs.CACHE_CONTROL] = "no-cache, must-revalidate"
        response.headers[hdrs.PRAGMA] = "no-cache"
        response.headers[hdrs.EXPIRES] = expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
        return response

    return middleware


async def not_robot(app, handler):
    async def middleware(request):
        response = await handler(request)
        response.headers['X-Robots-Tag'] = 'noindex, nofollow, noarchive, notranslate, noimageindex'
        response.headers['Accept-CH'] = 'device-memory, dpr, width, viewport-width, rtt, downlink, ect'
        response.headers['Accept-CH-Lifetime'] = '31536000'
        response.headers['Referrer-Policy'] = 'no-referrer'
        return response

    return middleware


async def customer_middleware(app, handler):
    async def middleware(request):
        request.is_customer = False
        ip = '127.0.0.1'
        ip_regex = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
        headers = request.headers
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
                peername = request.transport.get_extra_info('peername')
                if peername is not None and isinstance(peername, tuple):
                    ip, _ = peername
            except Exception as ex:
                logger.error(exception_message(exc=str(ex), request=str(request._message)))

        cookie_name = 'yottos_customer'
        request.ip = ip
        if request.cookies.get(cookie_name):
            request.is_customer = True

        if not request.is_customer:
            if ip_pattern.search(ip) is not None:
                request.is_customer = True

        response = await handler(request)
        return response

    return middleware


def setup_middlewares(app):
    error_middleware = error_pages({404: handle_404,
                                    405: handle_405,
                                    500: handle_500})
    app.middlewares.append(error_middleware)
    app.middlewares.append(cookie_middleware)
    app.middlewares.append(check_referer_middleware)
    app.middlewares.append(disable_cache_middleware)
    app.middlewares.append(not_robot)
    app.middlewares.append(detect_bot_middleware)
    app.middlewares.append(customer_middleware)
    app.middlewares.append(fingerprint_middleware)
