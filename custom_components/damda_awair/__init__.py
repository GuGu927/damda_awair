"""The Damda Awair integration."""
from __future__ import annotations
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import HomeAssistant

from .const import API_NAME, API_DEVICE, BRAND, DOMAIN, NAME, PLATFORMS
from .api_damda_awair import get_api, DamdaAwairAPI as API

_LOGGER = logging.getLogger(__name__)


def log(flag, val):
    """0:debug, 1:info, 2:warning, 3:error."""
    if flag == 0:
        _LOGGER.debug(f"[{BRAND}] {val}")
    elif flag == 1:
        _LOGGER.info(f"[{BRAND}] {val}")
    elif flag == 2:
        _LOGGER.warning(f"[{BRAND}] {val}")
    elif flag == 3:
        _LOGGER.error(f"[{BRAND}] {val}")


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Damda Awair from a config entry."""
    log(1, f"{NAME} Initialize")
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN].setdefault(API_DEVICE, {})
    api = get_api(hass)
    if api is None:
        api = API(hass)
        hass.data[DOMAIN][API_NAME] = api
    api.set_entry(entry)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    if hass.is_running:
        hass.async_add_executor_job(api.update, True)
    else:
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, api.update)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(API_DEVICE)
        hass.data[DOMAIN].pop(API_NAME)

    log(1, f"{NAME} Unload -> {unload_ok}")
    return unload_ok
