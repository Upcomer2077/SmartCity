from abc import ABC

import pytest
from transmitter.brokers import BaseBroker
from transmitter.brokers.kafka_ import KafkaBroker


class TestTransmitter:
    def test_is_broker_abstract(self):
        assert issubclass(BaseBroker, ABC)

    def test_is_broker_subclass(self):
        assert issubclass(KafkaBroker, BaseBroker)

    @pytest.mark.parametrize("broker", [KafkaBroker])
    def test_get_broker_name(self, broker):
        assert type(broker().get_broker_name()) is str

    @pytest.mark.asyncio
    @pytest.mark.parametrize("broker", [KafkaBroker])
    async def test_broker_not_none(self, broker: type[BaseBroker]):
        assert broker()._broker is not None
