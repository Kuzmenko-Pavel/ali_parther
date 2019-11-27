import aiohttp_jinja2
import jinja2


def init_templates(app):
    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('ali_partner', 'templates'))
