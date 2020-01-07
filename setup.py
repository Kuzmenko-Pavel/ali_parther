import os
import re

from setuptools import setup, find_packages


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__),
                           'ali_partner', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            msg = 'Cannot find version in ali_partner/__init__.py'
            raise RuntimeError(msg)


install_requires = ['aiohttp',
                    'aiodns',
                    'ujson',
                    'trafaret-config',
                    'pytz',
                    'aiohttp_jinja2',
                    'uvloop',
                    'cchardet',
                    'aiohttp_debugtoolbar',
                    'requests',
                    'pillow',
                    'ua-parser>=0.4.1',
                    ]

setup(
    name="ali_partner",
    version=read_version(),
    url="",
    packages=find_packages(),
    package_data={

    },
    install_requires=install_requires,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'link_check = console_scripts.link_checker:main',
        ],
    }
)
