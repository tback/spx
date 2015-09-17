#!/usr/bin/env python
import sys
import argparse
import logging

import spx


def main():
    common_parser = argparse.ArgumentParser(add_help=False)
    credentials = common_parser.add_argument_group('Credentials')
    credentials.add_argument('-u', '--username',
                             help='Username to authenticate against Smartplug')
    credentials.add_argument('-p', '--password',
                             help='Password to authenticate against Smartplug')
    logging_group = common_parser.add_argument_group('Logging')
    logging_group.add_argument('-l', '--loglevel',
                               choices=['DEBUG', 'INFO', 'WARNING', 'ERROR',
                                        'CRITICAL'],
                               default='ERROR', help='Loglevel')

    parser = argparse.ArgumentParser(parents=[common_parser])
    parser.add_argument('host', help='Hostname or IP of the Smartplug')
    # parser.add_argument('command', choices=['query', 'on', 'off', 'monitor'],
    #                     help='The command you\'re trying to send')

    subparsers = parser.add_subparsers(title='subcommands',
                                       help='additional help')
    off_parser = subparsers.add_parser('off', parents=[common_parser])
    off_parser.set_defaults(
        func=lambda args: spx.off(args.host, args.username, args.password))

    off_parser = subparsers.add_parser('on', parents=[common_parser])
    off_parser.set_defaults(
        func=lambda args: spx.on(args.host, args.username, args.password))

    monitor_parser = subparsers.add_parser('monitor', parents=[common_parser])
    monitor_parser.add_argument('-i', '--interval', type=int, default=5,
                                help='monitor interval in seconds')
    monitor_parser.set_defaults(
        func=lambda args: spx.monitor(args.host, args.interval, args.username,
                                      args.password))

    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.loglevel),
                        stream=sys.stderr)

    args.func(args)


if __name__ == '__main__':
    main()
