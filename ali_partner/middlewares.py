from datetime import datetime, timedelta

from aiohttp import web

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
        user_cookie_name = 'parther_unique_id'
        expires = datetime.utcnow() + timedelta(days=365)
        user_cookie_expires = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
        # user_cookie_domain = '*.yottos.com'
        user_cookie_max_age = 60 * 60 * 24 * 365
        try:
            user_cookie = int(request.cookies.get(user_cookie_name, 0))
        except Exception:
            user_cookie = 1

        if user_cookie > 0:
            request.not_uniq = True
        else:
            request.not_uniq = False

        user_cookie += 1
        request.user_cookie = user_cookie
        response = await handler(request)
        response.set_cookie(user_cookie_name, request.user_cookie, path='',
                            expires=user_cookie_expires, max_age=user_cookie_max_age, secure=True)
        try:
            response._cookies[user_cookie_name]['samesite'] = None
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
