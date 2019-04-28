"""
A component which allows you to get information about next departure from spesified stop.
For more details about this component, please refer to the documentation at
https://github.com/HalfDecent/HA-Custom_components/wienerlinien
"""
import logging
import requests
import dateutil.parser
import voluptuous as vol
from datetime import timedelta
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA

__version__ = '1.1.2'

CONF_STOPS = 'stops'
CONF_APIKEY = 'apikey'

ATTR_STOPID = 'stopid'
ATTR_NEXT_DEPARTURE = 'next_departure'
ATTR_FIRST_DEPARTURE = 'first_departure'
ATTR_COMPONENT = 'component'
ATTR_FRIENDLY_NAME = 'friendly_name'
ATTR_COMPONENT_VERSION = 'component_version'

SCAN_INTERVAL = timedelta(seconds=30)

ICON = 'mdi:bus'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_APIKEY): cv.string,
    vol.Optional(CONF_STOPS, default=None): 
        vol.All(cv.ensure_list, [cv.string]),
})

BASE_URL = 'http://www.wienerlinien.at/ogd_realtime/monitor'

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    stops = config.get(CONF_STOPS)
    apikey = config.get(CONF_APIKEY)
    dev = []
    for stopid in stops:
        dev.append(WienerlinienSensor(stopid, apikey))
    add_devices_callback(dev, True)

class WienerlinienSensor(Entity):
    def __init__(self, stopID, apikey):
        self._name = None
        self._state = None
        self._nextdeparture = 'N/A'
        self._firstdeparture = 'N/A'
        self._stopID = stopID
        self._apikey = apikey
        fetchurl = BASE_URL + '?rbl=' + self._stopID + '&sender=' + self._apikey
        departure = requests.get(fetchurl, timeout=5).json()['data']
        name = departure['monitors'][0]['locationStop']['properties']['title']
        self._name = name

    def update(self):
        fetchurl = BASE_URL + '?rbl=' + self._stopID + '&sender=' + self._apikey
        try:
            departure = requests.get(fetchurl, timeout=5).json()['data']
        except:
            _LOGGER.debug("Error fetching new state")
        else:
            try:
                departure['monitors'][0]['lines'][0]['departures']['departure'][0]['departureTime']['countdown']
            except:
                firstDeparture = 'N/A'
                nextDeparture = 'N/A'
            else:
                firstDeparture = departure['monitors'][0]['lines'][0]['departures']['departure'][0]['departureTime']['countdown']
                nextDeparture = departure['monitors'][0]['lines'][0]['departures']['departure'][1]['departureTime']['countdown']
            DepartureTowards = departure['monitors'][0]['lines'][0]['towards']
            FriendlyName = departure['monitors'][0]['locationStop']['properties']['title']
            if firstDeparture == 'N/A':
                self._state = DepartureTowards
            else: 
                self._state = ' ' + str(firstDeparture) + ' und in  ' + ' ' + str(nextDeparture) + ' Minuten Richtung '+ DepartureTowards
            self._firstdeparture = firstDeparture
            self._nextdeparture = nextDeparture

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return ICON

    @property
    def friendly_name(self):
        return self._fiendlyname

    @property
    def device_state_attributes(self):
        return {
            ATTR_FIRST_DEPARTURE: self._firstdeparture,
            ATTR_NEXT_DEPARTURE: self._nextdeparture,
            ATTR_STOPID: self._stopID,
        }
