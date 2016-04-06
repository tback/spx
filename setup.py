from distutils.core import setup

import re
import sys
from setuptools import find_packages

with open('spx/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

requires = [
    'apscheduler<4',
    'requests<3',
    'six',
]

if sys.version_info < (3, 3):
    # python started bundling in 3.3
    requires.extend([
        'mock'
    ])

setup(
    name='spx',
    version=version,
    install_requires=requires,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'spx-tool = spx.tool:SPXTool.run',
        ]
    },
    url='https://github.com/tback/spx',
    license='MIT',
    author='Till Backhaus',
    author_email='till@backha.us',
    description='Unofficial Python Library for Edimax Smartplugs SP-2101W and SP-1101W'
)
