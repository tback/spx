import datetime
import unittest
from unittest.mock import MagicMock, patch

from spx import Smartplug


class SmartplugTestCase(unittest.TestCase):
    @patch('spx.Smartplug._get_timestamp',
           return_value=datetime.datetime(2015, 9, 17, 14, 28, 1))
    @patch('requests.post', return_value=MagicMock())
    def test_get_usage(self, p, d):
        p.return_value.status_code = 200
        p.return_value.content = '<?xml version="1.0" encoding="UTF8"?><SMARTPLUG id="edimax">\n<CMD id="get">\n    <NOW_POWER><Device.System.Power.LastToggleTime>20150912160852</Device.System.Power.LastToggleTime><Device.System.Power.NowCurrent>0.0450</Device.System.Power.NowCurrent><Device.System.Power.NowPower>5.29</Device.System.Power.NowPower><Device.System.Power.NowEnergy.Day>0.080</Device.System.Power.NowEnergy.Day><Device.System.Power.NowEnergy.Week>0.080</Device.System.Power.NowEnergy.Week><Device.System.Power.NowEnergy.Month>1.214</Device.System.Power.NowEnergy.Month>\n    </NOW_POWER>\n</CMD>\n</SMARTPLUG>'
        plug = Smartplug('240.0.0.1')

        self.assertDictEqual(
            plug.get_usage(),
            {
                't': datetime.datetime(2015, 9, 17, 14, 28, 1),
                'current': 0.045,
                'day': 0.080,
                'last_toggle_time': datetime.datetime(2015, 9, 12, 16, 8, 52),
                'month': 1.214,
                'power': 5.29,
                'week': 0.080,
            }
        )
        p.assert_called_once_with(
            'http://admin:1234@240.0.0.1:10000/smartplug.cgi',
            data='\n<?xml version="1.0" encoding="UTF8"?>\n<SMARTPLUG id="edimax">\n<CMD id="get">\n    <NOW_POWER>\n    </NOW_POWER>\n</CMD>\n</SMARTPLUG>'        )


    @patch('requests.post', return_value=MagicMock())
    def test_set_state(self, p):
        p.return_value.status_code = 200
        p.return_value.content = '<?xml version="1.0" encoding="UTF8"?><SMARTPLUG id="edimax">\n<CMD id="setup">OK</CMD>\n</SMARTPLUG>'
        plug = Smartplug('240.0.0.1')

        self.assertTrue(plug.set_state('on'))

    @patch('requests.post', return_value=MagicMock())
    def test_get_state(self, p):
        p.return_value.status_code = 200
        p.return_value.content = '<?xml version="1.0" encoding="UTF8"?><SMARTPLUG id="edimax">\n<CMD id="get">\n    <Device.System.Power.State>OFF</Device.System.Power.State>\n</CMD>\n</SMARTPLUG>'
        plug = Smartplug('240.0.0.1')
        self.assertEquals(plug.get_state(), 'OFF')
