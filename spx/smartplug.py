# -*- coding: utf-8 -*-
import datetime
import logging
import re
import textwrap
import sys
from xml.dom.minidom import parseString

import requests
from apscheduler.schedulers.blocking import BlockingScheduler

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

    SET_STATE_MESSAGE = MESSAGE.format(command=textwrap.dedent('''
        <CMD id="setup">
            <Device.System.Power.State>{state}</Device.System.Power.State>
        </CMD>'''))

    GET_STATE_MESSAGE = MESSAGE.format(command=textwrap.dedent('''
        <CMD id="get">
            <Device.System.Power.State></Device.System.Power.State>
        </CMD>'''))

    GET_USAGE_MESSAGE = MESSAGE.format(command=textwrap.dedent('''
        <CMD id="get">
            <NOW_POWER>
            </NOW_POWER>
        </CMD>'''))

    BOOLEAN_STATES = {'1': True, 'yes': True, 'true': True, 'on': True,
                      '0': False, 'no': False, 'false': False, 'off': False}

    def __init__(self, host, username='admin', password='1234'):
        self.host = host
        self.username = username
        self.password = password

        self.url = self.URL.format(p=self)

    def _convert_to_boolean(self, value):
        """Return a boolean value translating from other types if necessary.
        """
        if type(value) is bool:
            return value
        if value.lower() not in self.BOOLEAN_STATES:
            raise ValueError('Not a boolean: %s' % value)
        return self.BOOLEAN_STATES[value.lower()]

    def _send_command(self, command):
        log.debug(command)
        response = requests.post(self.url, data=command)

        if response.status_code != 200:
            raise (
            SmartplugCommandFailed(response.status_code, response.content))

        log.debug(response.content)
        return response.content

    def get_state(self):
        self._send_command(self.GET_STATE_MESSAGE)

    def set_state(self, state):
        self._send_command(self.SET_STATE_MESSAGE.format(
            state='ON' if self._convert_to_boolean(state) else 'OFF'
        ))

    def switch(self, state):
        return self.set_state(state)

    def on(self):
        self.set_state(True)

    def off(self):
        self.set_state(False)

    def get_usage(self):
        response = self._send_command(self.GET_USAGE_MESSAGE)
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
            q=self.get_usage()
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


def get_state(host, username=None, password=None):
    return Smartplug(host, username=username, password=password).get_state()


def set_state(host, state, username=None, password=None):
    return Smartplug(host, username=username, password=password).set_state(
        state)


def switch(host, state, username=None, password=None):
    return Smartplug(host, username=username, password=password).switch(state)


def get_usage(host, username=None, password=None):
    return Smartplug(host, username=username, password=password).get_usage()


def monitor(host, interval=None, username=None, password=None):
    return Smartplug(host, username=username, password=password).monitor(
        interval)
