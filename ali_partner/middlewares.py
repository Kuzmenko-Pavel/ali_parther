from datetime import datetime, timedelta

from aiohttp import web

from random import randint

from ali_partner.logger import logger, exception_message


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
        rand_partner_id = randint(1, 2)
        #имя куки счетчика запросов
        partner_unique = 'pui'

        # имя куки партнера
        partner_id = 'pi'

        expires = datetime.utcnow() + timedelta(days=365)
        user_cookie_expires = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
        user_cookie_max_age = 60 * 60 * 24 * 365

        try:
            # получаю счетчик запросов
            request_count = int(request.cookies.get(partner_unique, 0 << 32)) >> 32

            # получаю партнера
            partner = int(request.cookies.get(partner_id, rand_partner_id << 32)) >> 32
        except Exception as e:
            #если чето левое было то дефолт
            request_count = 1
            partner = rand_partner_id

        #если счетчик больше 0, то не уник
        if request_count > 0:
            request.not_uniq = True
        else:
            request.not_uniq = False

        #инкремент счетчика
        request_count += 1

        #засунул в реквест чтобы дальше работать
        request.request_count = request_count
        request.partner = partner
        response = await handler(request)

        #пересоздал куку счетчика с новыми значениями
        response.set_cookie(partner_unique, request.request_count << 32, path='',
                            expires=user_cookie_expires, max_age=user_cookie_max_age, secure=True)

        # пересоздал куку партнера с новыми временем
        response.set_cookie(partner_id, request.partner << 32, path='',
                            expires=user_cookie_expires, max_age=user_cookie_max_age, secure=True)
        try:
            #костыль для поддержки samesite
            response._cookies[partner_unique]['samesite'] = None
            response._cookies[partner_id]['samesite'] = None
        except Exception:
            pass
        return response

    return middleware


async def check_referer_middleware(app, handler):
    async def middleware(request):
        headers = request.headers
        request.referer = headers.get('Referer', '')
        if 'rg.yottos.com' in request.referer:
            request.fail_referer = False
        else:
            request.fail_referer = True
        response = await handler(request)
        return response

    return middleware


async def disable_cache_middleware(app, handler):
    async def middleware(request):
        expiry_time = datetime.utcnow()
        response = await handler(request)
        response.headers["Cache-Control"] = "no-cache, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
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
