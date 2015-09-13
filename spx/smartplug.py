import datetime
import logging
import re
import textwrap
import requests
import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from xml.dom.minidom import parseString


log = logging.getLogger(__name__)


def un_camel(s):
    return re.sub(r'((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))',
                  r'_\1', s).lower()


class SmartplugException(Exception):
    pass


class SmartplugCommandFailed(SmartplugException):
    pass


class Smartplug(object):
    DATETIME_FORMAT = '%Y%m%d%H%M%S'

    URL = 'http://{p.username}:{p.password}@{p.host}:10000/smartplug.cgi'

    MESSAGE = textwrap.dedent('''
        <?xml version="1.0" encoding="UTF8"?>
        <SMARTPLUG id="edimax">{command}
        </SMARTPLUG>''')

    SWITCH_MESSAGE = MESSAGE.format(command=textwrap.dedent('''
        <CMD id="setup">
            <Device.System.Power.State>{state}</Device.System.Power.State>
        </CMD>'''))

    QUERY_MESSAGE_STATE = MESSAGE.format(command=textwrap.dedent('''
        <CMD id="get">
            <Device.System.Power.State></Device.System.Power.State>
        </CMD>'''))

    QUERY_MESSAGE = MESSAGE.format(command=textwrap.dedent('''
        <CMD id="get">
            <NOW_POWER>
            </NOW_POWER>
        </CMD>'''))

    def __init__(self, host, username='admin', password='1234'):
        self.host = host
        self.username = username
        self.password = password

        self.url = self.URL.format(p=self)

    def send_command(self, command):
        log.debug(command)
        response = requests.post(self.url, data=command)

        if response.status_code != 200:
            raise(SmartplugCommandFailed(response.status_code, response.content))

        log.debug(response.content)
        return response.content

    def on(self):
        self.send_command(self.SWITCH_MESSAGE.format(state='ON'))

    def off(self):
        self.send_command(self.SWITCH_MESSAGE.format(state='OFF'))

    def query(self):
        response = self.send_command(self.QUERY_MESSAGE)
        dom = parseString(response)
        dom_data = dom.getElementsByTagName('NOW_POWER')
        result = {}
        for node in dom_data[0].childNodes:
            if node.nodeType != node.ELEMENT_NODE:
                continue
            key = un_camel(re.sub('.*\.(Now)?', '', node.nodeName))
            value = node.firstChild.nodeValue.strip()
            result[key] = value
        return result

    def run_monitor(self):
        print('{timestamp} {q.power}'.format(
            timestamp=datetime.datetime.now().strftime(self.DATETIME_FORMAT),
            q=self.query()
        ))
        sys.stdout.flush()

    def monitor(self, interval=None):
        if interval is None:
            interval = 5
        if type(interval) is str:
            interval = int(interval)
        scheduler = BlockingScheduler()
        self.run_monitor()
        if interval < 1:
            return

        scheduler.add_job(self.run_monitor, 'interval', seconds=int(interval))

        try:
            scheduler.start()
        except KeyboardInterrupt:
            sys.exit(0)


def on(host, username=None, password=None):
    return Smartplug(host, username=username, password=password).on()


def off(host, username=None, password=None):
    return Smartplug(host, username=username, password=password).off()


def query(host, username=None, password=None):
    return Smartplug(host, username=username, password=password).query()


def monitor(host, repeat=None, username=None, password=None):
    return Smartplug(host, username=username, password=password).monitor(repeat)
