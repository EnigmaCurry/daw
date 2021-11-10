# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daw']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.24,<0.30.0',
 'pydub>=0.25.1,<0.26.0',
 'simpleaudio>=1.0.4,<2.0.0']

setup_kwargs = {
    'name': 'daw',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'EnigmaCurry',
    'author_email': 'ryan@enigmacurry.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
