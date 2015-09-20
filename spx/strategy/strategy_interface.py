from abc import ABCMeta, abstractmethod
from spx import Smartplug


class StrategyInterface(ABCMeta):
    @abstractmethod
    def update(self, d):
        """
        Add a datapoint
        :param d: datapoint
        :return: None
        """
        raise NotImplementedError()

    @abstractmethod
    def run(self, plug: Smartplug):
        """
        Add a datapoint
        :param plug: The Smartplug to control
        :return: None
        """
        raise NotImplementedError()
