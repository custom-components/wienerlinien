import logging
import copy
from custom_components.wienerlinien.sensor import WienerlinienSensor
from custom_components.wienerlinien.api import WienerlinienAPI

from .fixtures import stop_response, stopCallStub

_LOGGER = logging.getLogger(__name__)


async def test_event_on_setup(stopCallStub, hass):

    evcal = []

    def check_event(event):
        assert event.data.get("oldTime") == None
        assert event.data.get("newTime") == "2021-09-21T19:03:58.000+0200"
        assert event.data.get("line") == "12A"
        assert event.data.get("destination") == "Schmelz, Gablenzgasse"
        evcal.append(event)

    hass.bus.async_listen("wienerlinien_new_arrival", check_event)

    api = WienerlinienAPI(stopCallStub, None, "651")
    sensor = WienerlinienSensor(api, "test_0", 0, "first", hass.bus)

    await sensor.async_update()
    await hass.async_block_till_done()
    assert len(evcal) == 1


async def test_event_on_new_arrival(stopCallStub, hass):
    evcal = []

    def check_event(event):
        assert event.data.get("oldTime") == "2021-09-21T19:03:58.000+0200"
        assert event.data.get("newTime") == "2021-09-21T19:09:53.000+0200"
        assert event.data.get("line") == "12A"
        assert event.data.get("destination") == "Schmelz, Gablenzgasse"
        evcal.append(event)

    def dummy_handler(event):
        pass

    usub = hass.bus.async_listen("wienerlinien_new_arrival", dummy_handler)

    api = WienerlinienAPI(stopCallStub, None, "651")
    sensor = WienerlinienSensor(api, "test_0", 0, "first", hass.bus)
    await sensor.async_update()
    await hass.async_block_till_done()

    usub()

    old651 = copy.deepcopy(stop_response[651])
    del stop_response[651]["data"]["monitors"][0]["lines"][0]["departures"][
        "departure"
    ][0]

    hass.bus.async_listen("wienerlinien_new_arrival", check_event)
    await sensor.async_update()
    await hass.async_block_till_done()
    assert len(evcal) == 1

    del stop_response[651]
    stop_response[651] = old651


async def test_no_new_arrival_event(stopCallStub, hass):
    evcal = []

    def handler(event):
        evcal.append(event)

    hass.bus.async_listen("wienerlinien_new_arrival", handler)

    api = WienerlinienAPI(stopCallStub, None, "651")
    sensor = WienerlinienSensor(api, "test_0", 0, "first", hass.bus, False)
    await sensor.async_update()
    await hass.async_block_till_done()
    assert len(evcal) == 0
