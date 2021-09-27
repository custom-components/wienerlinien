import logging
from pytest_homeassistant_custom_component.common import AsyncMock
from pytest_homeassistant_custom_component.plugins import MagicMock
from custom_components.wienerlinien.sensor import WienerlinienSensor
from custom_components.wienerlinien.api import WienerlinienAPI


from .fixtures import stop_response, stopCallStub


async def test_async_update_failed():
    wiener_linien_api = MagicMock()
    wiener_linien_api.get_json = AsyncMock(return_value=None)

    sensor = WienerlinienSensor(wiener_linien_api, "test", 0, False)
    await sensor.async_update()

    assert sensor.state == None
    pass


async def test_async_update_ok(stopCallStub):
    api = WienerlinienAPI(stopCallStub, None, "651")
    sensor = WienerlinienSensor(api, "test_0", 0, "first")
    await sensor.async_update()

    time = "2021-09-21T19:03:58.000+0200"
    exp = f"{time[:-2]}:{time[26:]}"

    assert sensor.state == exp


_LOGGER = logging.getLogger(__name__)


async def test_seticon(stopCallStub):
    api = WienerlinienAPI(stopCallStub, None, "651")
    sensor = WienerlinienSensor(api, "test_0", 0, "first")
    await sensor.async_update()
    assert sensor.entity_picture == "/wienerlinien/icons/bus.svg"

    api = WienerlinienAPI(stopCallStub, None, "4939")
    sensor = WienerlinienSensor(api, "test_0", 0, "first")
    await sensor.async_update()
    assert sensor.entity_picture == "/wienerlinien/icons/U3.svg"

    api = WienerlinienAPI(stopCallStub, None, "3435")
    sensor = WienerlinienSensor(api, "test_0", 0, "first")
    await sensor.async_update()
    assert sensor.entity_picture == "/wienerlinien/icons/tram.svg"


async def test_alternate_monitors_on_sensor(stopCallStub):
    api = WienerlinienAPI(stopCallStub, None, "3435")
    sensor1 = WienerlinienSensor(api, "test_0", 0, "first")
    await sensor1.async_update()
    sensor2 = WienerlinienSensor(api, "test_0", 1, "first")
    await sensor2.async_update()

    assert sensor1.name == f"(11) test_0 first departure"
    assert sensor2.name == f"(6) test_0 first departure"
    assert sensor1.attributes["name"] == "11"
    assert sensor2.attributes["name"] == "6"
