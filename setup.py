from distutils.core import setup

setup(
    name='spx',
    version='0.1',
    install_requires=[
        'requests',
        'apscheduler',
        'six',
    ],
    packages=[''],
    url='https://bitbucket.org/tback/spx',
    license='MIT',
    author='Till Backhaus <till@backha.us>',
    author_email='till@backha.us',
    description='Unofficial Python Library for Edimax Smartplugs SP-2101W and SP-1101W'
)
