import unittest
from unittest.mock import MagicMock, patch
from spx import Smartplug


class SmartplugTestCase(unittest.TestCase):
    @patch('requests.post', return_value=MagicMock())
    def test_query(self, p):
        p.return_value.status_code = 200
        p.return_value.content = '<?xml version="1.0" encoding="UTF8"?><SMARTPLUG id="edimax">\n<CMD id="get">\n    <NOW_POWER><Device.System.Power.LastToggleTime>20150912160852</Device.System.Power.LastToggleTime><Device.System.Power.NowCurrent>0.0450</Device.System.Power.NowCurrent><Device.System.Power.NowPower>5.29</Device.System.Power.NowPower><Device.System.Power.NowEnergy.Day>0.080</Device.System.Power.NowEnergy.Day><Device.System.Power.NowEnergy.Week>0.080</Device.System.Power.NowEnergy.Week><Device.System.Power.NowEnergy.Month>1.214</Device.System.Power.NowEnergy.Month>\n    </NOW_POWER>\n</CMD>\n</SMARTPLUG>'
        plug = Smartplug('240.0.0.1')

        self.assertDictEqual(plug.get_usage(), {'current': '0.0450',
                                            'day': '0.080',
                                            'last_toggle_time': '20150912160852',
                                            'month': '1.214',
                                            'power': '5.29',
                                            'week': '0.080'})
    # def test_query(self, p):
    #     plug = Smartplug('notcalled')
    #     plug.send_command = MagicMock(return_value='<?xml version="1.0" encoding="UTF8"?><SMARTPLUG id="edimax">\n<CMD id="get">\n    <NOW_POWER><Device.System.Power.LastToggleTime>20150912160852</Device.System.Power.LastToggleTime><Device.System.Power.NowCurrent>0.0450</Device.System.Power.NowCurrent><Device.System.Power.NowPower>5.29</Device.System.Power.NowPower><Device.System.Power.NowEnergy.Day>0.080</Device.System.Power.NowEnergy.Day><Device.System.Power.NowEnergy.Week>0.080</Device.System.Power.NowEnergy.Week><Device.System.Power.NowEnergy.Month>1.214</Device.System.Power.NowEnergy.Month>\n    </NOW_POWER>\n</CMD>\n</SMARTPLUG>')
    #     self.assertDictEqual(plug.query(), {'current': '0.0450',
    #                                         'day': '0.080',
    #                                         'last_toggle_time': '20150912160852',
    #                                         'month': '1.214',
    #                                         'power': '5.29',
    #                                         'week': '0.080'})
    # def test_on(self):
    #     plug = Smartplug('notcalled')
    #     plug.send_command = MagicMock(return_value='<?xml version="1.0" encoding="UTF8"?><SMARTPLUG id="edimax">\n<CMD id="get">\n    <NOW_POWER><Device.System.Power.LastToggleTime>20150912160852</Device.System.Power.LastToggleTime><Device.System.Power.NowCurrent>0.0450</Device.System.Power.NowCurrent><Device.System.Power.NowPower>5.29</Device.System.Power.NowPower><Device.System.Power.NowEnergy.Day>0.080</Device.System.Power.NowEnergy.Day><Device.System.Power.NowEnergy.Week>0.080</Device.System.Power.NowEnergy.Week><Device.System.Power.NowEnergy.Month>1.214</Device.System.Power.NowEnergy.Month>\n    </NOW_POWER>\n</CMD>\n</SMARTPLUG>')
    #     self.assertDictEqual(plug.query(), {'current': '0.0450',
    #                                         'day': '0.080',
    #                                         'last_toggle_time': '20150912160852',
    #                                         'month': '1.214',
    #                                         'power': '5.29',
    #                                         'week': '0.080'})
    #
    # def test_off(self):
