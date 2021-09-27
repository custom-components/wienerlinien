""" Constant data for testing """

import json
import logging
import pytest
import re
from pytest_homeassistant_custom_component.common import load_fixture
from pytest_homeassistant_custom_component.common import AsyncMock, Mock
from pytest_homeassistant_custom_component.plugins import MagicMock

stop_response = {}
# stop_response[784] =
# stop_response[651] = json.loads(load_fixture("stop-651-data.json"))

stop_pattern = re.compile(
    "^http:\\/\\/www\\.wienerlinien\\.at\\/ogd_realtime\\/monitor\\?stopid=(\\d*)$"
)

LOGGER = logging.getLogger(__name__)


def getStopResponse(id: int) -> dict:
    if not id in stop_response:
        stop_response[id] = json.loads(load_fixture(f"stop-{id}-data.json"))
    return stop_response[id]


def provideStopFixture(url):
    stopid = int(stop_pattern.match(url)[1])

    response = Mock()
    response.json = AsyncMock(return_value=getStopResponse(stopid))
    return response


@pytest.fixture
def stopCallStub():
    session = MagicMock()
    session.get = AsyncMock(side_effect=provideStopFixture)
    return session
