#!/usr/bin/env python
from collections import deque
import sys
import argparse
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
import time

import spx


class SPXTool(object):
    DATETIME_FORMAT = '%Y%m%d%H%M%S'
    DEFAULT_INTERVAL = 5

    FORMATS = {
        'minimal': '{t:' + DATETIME_FORMAT + '} {power}',
        'default': '{t:' + DATETIME_FORMAT +'} {current} {power} {last_toggle_time:' + DATETIME_FORMAT + '}',
    }

    @staticmethod
    def run():
        SPXTool()()

    def __init__(self):
        self.args = None
        self.parse_args()
        self.history = None
        self.smartplug = spx.Smartplug(self.args.host,
                                       self.args.username, self.args.password)

    def __call__(self):
        self.args.func()

    def run_monitor(self, control, interval, threshould, timeframe):
        usage = self.smartplug.get_usage()
        print(self.FORMATS['default'].format(**usage))
        sys.stdout.flush()
        if control:
            if self.history is None:
                self.history = deque(maxlen=int(timeframe/interval))
            self.history.append(usage)
            if (len(self.history) == self.history.maxlen
                and max(self.history, key=lambda x: x['power'])['power'] < threshould):
                print('POWERCYCLE')
                sys.stdout.flush()
                self.history.clear()
                self.smartplug.off()
                time.sleep(3)
                self.smartplug.on()



    def monitor(self, interval=None, control=None, control_threshould=None, control_timeframe=None):
        if interval is None:
            interval = self.DEFAULT_INTERVAL
        if type(interval) is str:
            interval = int(interval)
        scheduler = BlockingScheduler()

        self.run_monitor(control, interval, control_threshould, control_timeframe)
        if interval < 1:
            return

        scheduler.add_job(lambda: self.run_monitor(control, interval, control_threshould, control_timeframe),
                          'interval',
                          seconds=int(interval))

        try:
            scheduler.start()
        except KeyboardInterrupt:
            sys.exit(0)

    def parse_args(self):
        common_parser = argparse.ArgumentParser(add_help=False)

        c_group = common_parser.add_argument_group('Credentials')
        c_group.add_argument(
            '-u', '--username',
            default=spx.Smartplug.DEFAULT_USERNAME,
            help='Username to authenticate against Smartplug'
        )

        c_group.add_argument(
            '-p', '--password',
            default=spx.Smartplug.DEFAULT_PASSWORD,
            help='Password to authenticate against Smartplug'
        )

        l_group = common_parser.add_argument_group('Logging')
        l_group.add_argument(
            '-l', '--loglevel',
            choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
            default='ERROR',
            help='Log level'
        )

        parser = argparse.ArgumentParser(parents=[common_parser])
        parser.add_argument('host', help='Hostname or IP of the Smartplug')

        commands = parser.add_subparsers(
            title='Commands',
            help='Description'
        )
        get_state_command = commands.add_parser(
            'get_state', parents=[common_parser],
            help='Get state of Smartplug (on or off)'
        )

        def f():  # cannot use print in lambda on python2
            print(self.smartplug.get_state())
        get_state_command.set_defaults(func=f)

        set_state_command = commands.add_parser(
            'set_state', parents=[common_parser],
            help='Set state of Smartplug (on or off)'
        )
        set_state_command.add_argument(
            'state',
            type=str.lower,
            choices=spx.Smartplug.BOOLEAN_STATES.keys(),
        )
        set_state_command.set_defaults(func=lambda: self.smartplug.set_state(self.args.state))

        on_command = commands.add_parser(
            'on', parents=[common_parser],
            help='Alias for set_state on'
        )
        on_command.set_defaults(func=lambda: self.smartplug.on())

        off_command = commands.add_parser(
            'off', parents=[common_parser],
            help='Alias for set_state off'
        )
        off_command.set_defaults(func=lambda: self.smartplug.off())

        switch_command = commands.add_parser(
            'switch', parents=[common_parser], help='Alias for set_state'
        )
        switch_command.add_argument(
            'state', type=str.lower, choices=spx.Smartplug.BOOLEAN_STATES.keys(),)
        switch_command.set_defaults(func=lambda: self.smartplug.set_state(self.args.state))

        monitor_command = commands.add_parser('monitor', parents=[common_parser],
            help='Monitor power usage'
        )
        monitor_command.add_argument(
            '-i', '--interval', type=int, default=self.DEFAULT_INTERVAL,
            help='monitor interval in seconds'
        )
        monitor_command.add_argument(
            '-f', '--format', default=self.FORMATS['default'],
        )
        monitor_command.add_argument(
            '-c', '--control', action='store_true',
            help='power cycle when consumption never exceeded a threshould for a time frame'
        )
        monitor_command.add_argument(
            '--control-timeframe', type=int, default=3600,
            help='control timeframe in seconds. Default: 3600s (1h)'
        )
        monitor_command.add_argument(
            '--control-threshould', type=int, default=50,
            help='control threhould in watt. Default: 50W'
        )
        monitor_command.set_defaults(
            func=lambda: self.monitor(self.args.interval, self.args.control, self.args.control_threshould, self.args.control_timeframe)
        )

        self.args = parser.parse_args()

        logging.basicConfig(level=getattr(logging, self.args.loglevel),
                            stream=sys.stderr)


if __name__ == '__main__':
    SPXTool()()
