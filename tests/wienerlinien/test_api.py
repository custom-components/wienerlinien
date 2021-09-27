import logging
from pytest_homeassistant_custom_component.common import AsyncMock, Mock
from pytest_homeassistant_custom_component.plugins import MagicMock
from custom_components.wienerlinien.sensor import WienerlinienSensor
from custom_components.wienerlinien.api import WienerlinienAPI


from .fixtures import stop_response, stopCallStub

async def test_async_update_ok(stopCallStub):

    api = WienerlinienAPI(stopCallStub, None, "784")
    val = await api.get_json()
    assert val == stop_response[784]
    pass


async def test_async_update_ok_other_stop(stopCallStub):

    api = WienerlinienAPI(stopCallStub, None, "651")
    val = await api.get_json()
    assert val == stop_response[651]
    pass
