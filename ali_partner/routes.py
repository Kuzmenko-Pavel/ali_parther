from .views import ApiView


def setup_routes(app):
    app.router.add_route('GET', '/{tail:.*}', ApiView)
    app.router.add_route('HEAD', '/{tail:.*}', ApiView)
