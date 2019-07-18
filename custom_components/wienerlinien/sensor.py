"""
A component which allows you to get information about next departure from spesified stop.
For more details about this component, please refer to the documentation at
https://github.com/custom-components/wienerlinien
"""
import logging
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
import async_timeout
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.exceptions import PlatformNotReady
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.entity import Entity

from .const import BASE_URL, DEPARTURES

CONF_STOPS = "stops"
CONF_APIKEY = "apikey"
CONF_FIRST_NEXT = "firstnext"

SCAN_INTERVAL = timedelta(seconds=30)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_APIKEY): cv.string,
        vol.Optional(CONF_STOPS, default=None): vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(CONF_FIRST_NEXT, default="first"): cv.string,
    }
)


_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Setup."""
    stops = config.get(CONF_STOPS)
    apikey = config.get(CONF_APIKEY)
    firstnext = config.get(CONF_FIRST_NEXT)
    dev = []
    for stopid in stops:
        api = CallAPI(async_create_clientsession(hass), hass.loop, apikey, stopid)
        data = await api.get_json()
        try:
            name = data["data"]["monitors"][0]["locationStop"]["properties"]["title"]
        except Exception:
            raise PlatformNotReady()
        dev.append(WienerlinienSensor(api, name, firstnext))
    add_devices_callback(dev, True)


class WienerlinienSensor(Entity):
    """WienerlinienSensor."""

    def __init__(self, api, name, firstnext):
        """Initialize."""
        self.api = api
        self.firstnext = firstnext
        self._name = name
        self._state = None
        self.attributes = {}

    async def async_update(self):
        """Update data."""
        try:
            data = await self.api.get_json()
            _LOGGER.debug(data)
            if data is None:
                return
            data = data.get("data", {})
        except:
            _LOGGER.debug("Could not get new state")
            return

        if data is None:
            return
        try:
            line = data["monitors"][0]["lines"][0]
            departure = line["departures"]["departure"][
                DEPARTURES[self.firstnext]["key"]
            ]
            self._state = departure["departureTime"]["timeReal"]

            self.attributes = {
                "destination": line["towards"],
                "platform": line["platform"],
                "direction": line["direction"],
                "name": line["name"],
                "countdown": departure["departureTime"]["countdown"],
            }
        except Exception:
            pass

    @property
    def name(self):
        """Return name."""
        return DEPARTURES[self.firstnext]["name"].format(self._name)

    @property
    def state(self):
        """Return state."""
        return self._state

    @property
    def icon(self):
        """Return icon."""
        return "mdi:bus"

    @property
    def device_state_attributes(self):
        """Return attrubutes."""
        return self.attributes

    @property
    def device_class(self):
        """Return device_class."""
        return "timestamp"


class CallAPI:
    """Call API."""

    def __init__(self, session, loop, apikey, stopid):
        """Initialize."""
        self.session = session
        self.loop = loop
        self.apikey = apikey
        self.stopid = stopid

    async def get_json(self):
        """Get json from API endpoint."""
        value = None
        url = BASE_URL.format(self.stopid, self.apikey)
        try:
            async with async_timeout.timeout(10, loop=self.loop):
                response = await self.session.get(url)
                value = await response.json()
        except Exception:
            pass

        return value
