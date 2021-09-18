from pytest_homeassistant_custom_component.common import AsyncMock, Mock
from pytest_homeassistant_custom_component.plugins import MagicMock
from custom_components.wienerlinien.sensor import WienerlinienSensor


async def test_async_update_failed():
    wiener_linien_api = MagicMock()
    wiener_linien_api.get_json = AsyncMock(return_value=None)

    sensor = WienerlinienSensor(wiener_linien_api, "test", 0, False)
    await sensor.async_update()

    assert sensor.state == None
    pass


async def test_async_update_ok():
    pass
