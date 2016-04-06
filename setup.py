from distutils.core import setup
import sys
from setuptools import find_packages

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
    version='0.2.0',
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
