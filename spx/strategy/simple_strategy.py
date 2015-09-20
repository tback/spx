import collections
import logging
from spx import Smartplug
from .strategy_interface import StrategyInterface

log = logging.getLogger(__name__)


class SimpleStrategy(StrategyInterface):
    """
    A very simple control strategy. It could be named the
    DidYouTryTurningItOffAndOnAgainStrategy.

    If a consumer never draws more than a given amount of power during a
    given time frame it is considered to be in errornous state and therefore
    power cycled.

    This strategy won't act until update has been called history_size times

    :param history_size the data points added through this many calls to update
    are considered in the Strategy
    :param limit the minimum amount power in watts that has to be drawn for the
    device to be considered active.
    :param cycle_duration stay off for this many seconds on error.

    """
    def __init__(self, history_size, limit, cycle_duration):
        self.history = collections.deque(maxlen=history_size)
        self.limit = limit
        self.cycle_duration = cycle_duration
        self.in_cycle = 0

    def update(self, d):
        self.history.append(d)

    def run(self, plug: Smartplug):
        if len(self.history) != self.history.maxlen:
            return

        if (not self.in_cycle
                and max(x.get('power', 0.0) for x in self.history) < self.limit):
            plug.off()
            self.in_cycle = self.cycle_duration
        else:
            self.in_cycle -= 1
            if self.in_cycle == 0:
                plug.on()
