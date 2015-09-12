#!/usr/bin/env python
import datetime
import requests
import re
import sys
import threading

HEIZUNG_URL='http://admin:1234@192.168.178.5:10000/smartplug.cgi'
ON='<?xml version="1.0" encoding="UTF8"?><SMARTPLUG id="edimax"><CMD id="setup"><Device.System.Power.State>ON</Device.System.Power.State></CMD></SMARTPLUG>'
OFF='<?xml version="1.0" encoding="UTF8"?><SMARTPLUG id="edimax"><CMD id="setup"><Device.System.Power.State>OFF</Device.System.Power.State></CMD></SMARTPLUG>'
QUERY='<?xml version="1.0" encoding="UTF8"?><SMARTPLUG id="edimax"><CMD id="get"><NOW_POWER><Device.System.Power.NowPower></Device.System.Power.NowPower></NOW_POWER></CMD></SMARTPLUG>'

def get_wattage(edimax_url):
    response = requests.post(edimax_url,data=QUERY)
    if response.status_code != 200:
        print('error', response)
        sys.exit(1)
    watt = re.search(br'\<Device\.System\.Power\.NowPower\>(?P<watt>.*)\<\/Device\.System\.Power\.NowPower\>',response.content).groupdict()['watt']
    return watt.decode('utf-8')

def print_watt(repeat=0):
    if(repeat!=0):
        threading.Timer(repeat, lambda: print_watt(repeat)).start()
    print('{timestamp} {wattage}'.format(timestamp=datetime.datetime.now().isoformat(), wattage=get_wattage(HEIZUNG_URL)))
    sys.stdout.flush()

def main():
    print_watt(int(sys.argv[1]))

if __name__ == '__main__':
    main()
