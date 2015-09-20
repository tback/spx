from distutils.core import setup
from setuptools import find_packages

setup(
    name='spx',
    version='0.2.0',
    install_requires=[
        'requests',
        'apscheduler',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'spx-tool = spx.tool:SPXTool.run',
        ]
    },
    url='https://bitbucket.org/tback/spx',
    license='MIT',
    author='Till Backhaus',
    author_email='till@backha.us',
    description='Unofficial Python Library for Edimax Smartplugs SP-2101W and SP-1101W'
)
