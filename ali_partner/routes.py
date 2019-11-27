from .views import ApiView


def setup_routes(app):
    app.router.add_route('GET', '/', ApiView)
    app.router.add_route('POST', '/', ApiView)
    app.router.add_static('/static/', app['config']['dir_path'] + '/static/', append_version=True)