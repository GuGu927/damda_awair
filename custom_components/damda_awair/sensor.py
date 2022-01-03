"""Damda Awair's sensor entity."""
from datetime import timedelta
from homeassistant.core import callback
from .device_damda_awair import DAwairDevice
from homeassistant.components.sensor import SensorEntity
from .api_damda_awair import get_api

from .const import (
    DEVICE_CLASS,
    DEVICE_ICON,
    DEVICE_UNIQUE,
    DEVICE_UNIT,
    NAME,
    SENSOR_DOMAIN,
)
import logging

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=30)


def log(flag, val):
    """0:debug, 1:info, 2:warning, 3:error."""
    if flag == 0:
        _LOGGER.debug(f"[{NAME}] Sensor > {val}")
    elif flag == 1:
        _LOGGER.info(f"[{NAME}] Sensor > {val}")
    elif flag == 2:
        _LOGGER.warning(f"[{NAME}] Sensor > {val}")
    elif flag == 3:
        _LOGGER.error(f"[{NAME}] Sensor > {val}")


def isfloat(value):
    """Determine string is float."""
    try:
        float(value)
        return True
    except ValueError:
        return False


def isnumber(value):
    """Determine string is number."""
    return (
        value is not None
        and isinstance(value, (str, int, float))
        and (
            isinstance(value, str)
            and (value.isnumeric() or value.isdigit())
            or isfloat(value)
        )
    )


def isnumber(value):
    """Determine string is number."""
    return (
        value is not None
        and isinstance(value, (str, int, float))
        and (
            isinstance(value, str)
            and (value.isnumeric() or value.isdigit())
            or isfloat(value)
        )
    )


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up sensor for Damda Awair component."""

    @callback
    def async_add_entity(devices=[]):
        """Add sensor from api_damda_awair."""
        entities = []
        api = get_api(hass)
        if api:
            try:
                if len(devices) == 0:
                    devices = api.sensors()
            except Exception:
                devices = []
            for device in devices:
                if DEVICE_UNIQUE not in device:
                    continue
                if not api.search_entity(SENSOR_DOMAIN, device[DEVICE_UNIQUE]):
                    entities.append(DAwairSensor(device, api))

        if entities:
            async_add_entities(entities)

    api = get_api(hass)
    if api:
        api.load(SENSOR_DOMAIN, async_add_entity)

    async_add_entity()


class DAwairSensor(DAwairDevice, SensorEntity):
    """Representation of a Damda Awair sensor."""

    TYPE = SENSOR_DOMAIN

    @property
    def state(self):
        """Return the state of the sensor."""
        state = self.api.get_state(self.unique_id)
        return state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        value = self.api.get_state(self.unique_id, DEVICE_ICON)
        return value

    @property
    def device_class(self):
        """Return the class of the sensor."""
        value = self.api.get_state(self.unique_id, DEVICE_CLASS)
        return value

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this sensor."""
        value = self.api.get_state(self.unique_id, DEVICE_UNIT)
        return value

    @property
    def state_class(self):
        """Type of this sensor state."""
        return "measurement" if isnumber(self.state) else None

    @property
    def should_poll(self) -> bool:
        """Verify poll."""
        return "_updatetime" in self.unique_id

    async def async_update(self):
        """Update API."""
        await self.api.update_awair(self.device_uuid)
