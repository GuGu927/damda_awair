"""Config flow for Damda Awair."""
import re
import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_IP_ADDRESS

from homeassistant import config_entries
from homeassistant.helpers.typing import DiscoveryInfoType

from .api_damda_awair import get_api, DamdaAwairAPI as API
from .const import API_NAME, DOMAIN, NAME_KOR

IP_REGEX = r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS): cv.string,
    }
)

_LOGGER = logging.getLogger(__name__)


def is_ip(v):
    """Return gateway connection type."""
    return re.search(IP_REGEX, v)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Damda Awair."""

    VERSION = 1

    def __init__(self):
        """Initialize the Damda Awair config flow."""
        self.discovered = False
        self.api = None

    async def get_awair(self, addr: str, is_manual: bool):
        """Get awair device uuid and try configure."""
        self.hass.data.setdefault(DOMAIN, {})
        self.api = get_api(self.hass)
        if self.api is None:
            self.discovered = True
            self.api = API(self.hass)
            self.hass.data[DOMAIN][API_NAME] = self.api
        setting = await self.api.get_setting(addr)
        uuid = setting.get("device_uuid")
        if uuid and not self.api.search_awair(uuid):
            await self.api.add_awair(uuid, setting)
            if is_manual:
                self.api.insert_awair(addr)

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=STEP_USER_DATA_SCHEMA,
                errors={},
            )
        ip = user_input.get(CONF_IP_ADDRESS)
        if not is_ip(ip):
            return self.async_abort(
                reason="not_ip_address", description_placeholders={"ip": ip}
            )
        await self.get_awair(ip, True)
        unique_id = await self.async_set_unique_id(DOMAIN)
        if unique_id is not None:
            return self.async_abort(
                reason="add_complete", description_placeholders={"ip": ip}
            )
        return self.async_create_entry(title=NAME_KOR, data={})

    async def async_step_add_awair(self, user_input=None):
        """Handle the initial step."""
        unique_id = await self.async_set_unique_id(DOMAIN)
        if unique_id is not None:
            return self.async_abort(reason="discovery_complete")
        return self.async_create_entry(title=NAME_KOR, data={})

    async def async_step_zeroconf(self, discovery_info: DiscoveryInfoType):
        """Handle a flow initialized by zeroconf discovery."""
        ip = discovery_info.get("host")
        if ip:
            await self.get_awair(ip, False)
            return await self.async_step_discovery(discovery_info)

    async def async_step_dhcp(self, discovery_info: DiscoveryInfoType):
        """Handle a flow initialized by zeroconf discovery."""
        ip = discovery_info.get("ip")
        if ip:
            await self.get_awair(ip, False)
            return await self.async_step_discovery(discovery_info)

    async def async_step_discovery(self, discovery_info: DiscoveryInfoType):
        """Handle a flow initialized by discovery."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        if discovery_info is not None:
            self.discovered = True
            return self.async_show_form(step_id="add_awair", errors={})
        return self.async_create_entry(title=NAME_KOR, data={})
