"""API for damda awair."""
import logging
import requests
from zoneinfo import ZoneInfo

from homeassistant.core import callback
from homeassistant.helpers.dispatcher import (
    async_dispatcher_connect,
    async_dispatcher_send,
)
from .const import (
    API_DEVICE,
    AWAIR_DEVICE,
    AWAIR_ITEM,
    BRAND,
    DATA_URL,
    DEVICE_ATTR,
    DEVICE_CLASS,
    DEVICE_DOMAIN,
    DEVICE_ENTITY,
    DEVICE_ICON,
    DEVICE_ID,
    DEVICE_NAME,
    DEVICE_REG,
    DEVICE_STATE,
    DEVICE_UNIQUE,
    DEVICE_UNIT,
    DEVICE_UPDATE,
    DOMAIN,
    API_NAME,
    MANUFACTURER,
    MODEL,
    NAME,
    NAME_KOR,
    SETTING_URL,
    SENSOR_DOMAIN,
    VERSION,
)


_LOGGER = logging.getLogger(__name__)
ZONE = ZoneInfo("Asia/Seoul")


@callback
def get_api(hass):
    """Return gateway with a matching entry_id."""
    hass.data.setdefault(DOMAIN, {})
    return hass.data[DOMAIN].get(API_NAME)


def log(flag, val):
    """0:debug, 1:info, 2:warning, 3:error."""
    if flag == 0:
        _LOGGER.debug(f"[{NAME}] {val}")
    elif flag == 1:
        _LOGGER.info(f"[{NAME}] {val}")
    elif flag == 2:
        _LOGGER.warning(f"[{NAME}] {val}")
    elif flag == 3:
        _LOGGER.error(f"[{NAME}] {val}")


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


class DamdaAwairAPI:
    """Damda Awair API."""

    def __init__(self, hass):
        """Initialize the Awair API."""
        self.hass = hass
        self.entry = None
        self.device = {}
        self.entities = {SENSOR_DOMAIN: {}}  # unique_id: True/False
        self.loaded = {SENSOR_DOMAIN: False}
        self.listeners = []
        self._start = False

        self.awair = {}
        self.awair_list = (
            self.get_data("awair_list", []) if self.entry is not None else []
        )
        self.log(1, "Loading API")

    def set_entry(self, entry):
        """Set entry."""
        self.entry = entry
        awair_list = self.awair_list + self.get_data("awair_list", [])
        self.awair_list = self.set_data("awair_list", list(dict.fromkeys(awair_list)))

    async def get_setting(self, ip):
        """Get device setting."""
        data = {}
        response = await self.hass.async_add_executor_job(
            requests.get, SETTING_URL.format(ip)
        )
        try:
            data = response.json()
        except Exception as ex:
            self.log(3, f"Error at get_setting > {ip} > {ex}")
        return data

    def search_awair(self, uuid):
        """Search awair via uuid address."""
        return self.awair.get(uuid)

    async def add_awair(self, uuid, info={}):
        """Add awair via uuid address."""
        if not self.awair.get(uuid):
            self.log(1, f"Find device > {uuid} > {info.get('ip')}")
            self.awair.setdefault(uuid, info)
            await self.update_awair(uuid)

    def insert_awair(self, ip):
        """Insert IP address at device list."""
        if ip not in self.awair_list:
            self.awair_list = self.awair_list + [ip]
            if self.entry is not None:
                self.set_data("awair_list", self.awair_list + [ip])

    def load(self, domain, async_add_entity):
        """Component loaded."""
        self.loaded[domain] = True
        self.listeners.append(
            async_dispatcher_connect(
                self.hass, self.async_signal_new_device(domain), async_add_entity
            )
        )
        if self.complete and not self._start:
            self._start = True
        self.log(1, f"Component loaded -> {domain}")

    @property
    def complete(self):
        """Component loaded."""
        for v in self.loaded.values():
            if not v:
                return False
        return True

    def log(self, level, msg):
        """Log."""
        log(level, msg)

    def set_data(self, key, value):
        """Set entry data."""
        self.hass.config_entries.async_update_entry(
            entry=self.entry, data={**self.entry.data, key: value}
        )
        return value

    def get_data(self, key, default=False):
        """Get entry data."""
        return self.entry.data.get(key, default)

    @property
    def manufacturer(self) -> str:
        """Get manufacturer."""
        return MANUFACTURER

    @property
    def version(self) -> str:
        """Get version."""
        return VERSION

    @property
    def brand(self) -> str:
        """Get brand."""
        return BRAND

    @property
    def name(self) -> str:
        """Get name."""
        return NAME_KOR

    @property
    def model(self) -> str:
        """Get model."""
        return MODEL

    def async_signal_new_device(self, device_type) -> str:
        """Damda Awair specific event to signal new device."""
        new_device = {
            SENSOR_DOMAIN: "damda_awair_new_sensor",
        }
        return new_device[device_type]

    def async_add_device(self, device=None, force: bool = False) -> None:
        """Handle event of new device creation in damda_awair."""

        if device is None or not isinstance(device, dict):
            return
        args = []
        unique_id = device.get(DEVICE_UNIQUE, None)
        domain = device.get(DEVICE_DOMAIN)
        if (
            self.search_entity(domain, unique_id)
            or not self.loaded.get(domain, False)
            or unique_id in self.hass.data[DOMAIN][API_DEVICE]
        ):
            return

        args.append([device])

        async_dispatcher_send(self.hass, self.async_signal_new_device(domain), *args)

    def sensors(self):
        """Get sensors."""
        target = SENSOR_DOMAIN
        return self.get_entities(target)

    def init_device(self, unique_id, domain, device=None):
        """Init device."""
        init_info = {
            DEVICE_DOMAIN: domain,
            DEVICE_REG: self.register_update_state,
            DEVICE_UPDATE: None,
            DEVICE_UNIQUE: unique_id,
            DEVICE_ENTITY: device,
        }
        if domain in self.entities:
            self.entities[domain].setdefault(unique_id, False)
        if unique_id not in self.device:
            self.log(0, f"Initialize device > {domain} > {unique_id}")
        return self.device.setdefault(unique_id, init_info)

    def make_entity(
        self, attr, icon, device_class, domain, state, unit, unique_id, entity_id, name
    ):
        """Make entity."""
        entity = {
            DEVICE_ATTR: {},
            DEVICE_DOMAIN: domain,
            DEVICE_STATE: state,
            DEVICE_UNIQUE: unique_id,
            DEVICE_ID: entity_id,
            DEVICE_NAME: name,
        }
        if attr is not None:
            entity[DEVICE_ATTR].update(attr)
        if unit is not None:
            entity[DEVICE_UNIT] = unit
        if icon is not None:
            entity[DEVICE_ICON] = icon
        if device_class is not None:
            entity[DEVICE_CLASS] = device_class
        if state is None:
            entity.pop(DEVICE_STATE)
        return entity

    def search_device(self, unique_id):
        """Search self.device."""
        return self.device.get(unique_id)

    def search_entity(self, domain, unique_id):
        """Search self.entities domain unique_id."""
        return self.entities.get(domain, {}).get(unique_id, False)

    def registered(self, unique_id):
        """Check unique_id is registered."""
        device = self.search_device(unique_id)
        return device.get(unique_id).get(DEVICE_UPDATE) is not None if device else False

    def get_entities(self, domain):
        """Get self.device from self.entites domain."""
        entities = []
        entity_list = self.entities.get(domain, {})
        for id in entity_list.keys():
            device = self.search_device(id)
            if device:
                entities.append(device)
            else:
                entities.append(self.init_device(id, domain))
        return entities

    def set_entity(self, domain, unique_id, state=False):
        """Set self.entities domain unique_id True/False."""
        if domain not in self.entities:
            self.log(1, f"set_entity > {domain} not exist.")
            pass
        if unique_id not in self.entities[domain]:
            self.log(1, f"set_entity > {domain} > {unique_id} not exist.")
            pass
        if state:
            self.entities[domain][unique_id] = state
            self.hass.data[DOMAIN][API_DEVICE][unique_id] = state
        # else:
        #     self.entities[domain].pop(unique_id)
        #     self.hass.data[DOMAIN][API_DEVICE].pop(unique_id)

    def get_state(self, unique_id, target=DEVICE_STATE):
        """Get device state."""
        device = self.search_device(unique_id)
        return device.get(DEVICE_ENTITY).get(target, None) if device else None

    def set_device(self, unique_id, entity):
        """Set device entity."""
        device = self.search_device(unique_id)
        if device:
            try:
                self.device[unique_id][DEVICE_ENTITY].update(entity)
            except Exception as ex:
                self.log(3, f"Set entity error > {unique_id} > {entity} > {ex}")

    def register_update_state(self, unique_id, cb=None):
        """Register device update function to update entity state."""
        device = self.search_device(unique_id)
        if device:
            if (device.get(DEVICE_UPDATE) is None and cb is not None) or (
                device.get(DEVICE_UPDATE) is not None and cb is None
            ):
                msg = f"{'Register' if cb is not None else 'Unregister'} device  => {unique_id}"
                self.log(0, msg)
                self.device[unique_id][DEVICE_UPDATE] = cb

    def update_entity(self, unique_id, entity, available=True):
        """Update device state."""
        device = self.search_device(unique_id)
        if not device:
            return
        self.device[unique_id][DEVICE_ENTITY].update(entity)
        if device.get(DEVICE_UPDATE) is not None:
            device.get(DEVICE_UPDATE)(available)
        else:
            self.async_add_device(device)

    async def get_airdata(self, ip):
        """Get air data from ip."""
        data = {}
        response = await self.hass.async_add_executor_job(
            requests.get, DATA_URL.format(ip)
        )
        try:
            data = response.json()
        except Exception as ex:
            self.log(3, f"Error at get_airdata > {ip} > {ex}")
        return data

    async def get_awair(self, info={}):
        """Patch from awair."""
        data = await self.get_airdata(info.get("ip"))
        uuid = info.get("device_uuid")
        awair_type = uuid.split("_")[0]
        result = {}
        self.log(0, f"Get data from Awair > {uuid} > {data}")
        for k, v in data.items():
            device_type = AWAIR_DEVICE.get(awair_type)
            if device_type is None or (device_type is not None and k in device_type):
                t = AWAIR_ITEM.get(k)
                icon = t[4] if t is not None else None
                device_class = t[5] if t is not None else None
                domain = t[3] if t is not None else SENSOR_DOMAIN
                unit = t[2] if t is not None else None
                unique_id = f"{uuid}_{t[0]}" if t is not None else f"{uuid}_{k}"
                entity_id = f"{uuid}_{t[0]}" if t is not None else f"{uuid}_{k}"
                entity_name = f"{uuid} {t[1]}" if t is not None else f"{uuid}_{k}"
                state = t[6](v) if t is not None and t[6] is not None else v
                entity = self.make_entity(
                    info,
                    icon,
                    device_class,
                    domain,
                    state,
                    unit,
                    unique_id,
                    entity_id,
                    entity_name,
                )
                result[unique_id] = entity
        return result

    async def update_awair(self, uuid):
        """Update result."""
        result = {}
        if self.search_awair(uuid) is not None:
            result = await self.get_awair(self.awair.get(uuid))
            self.log(0, f"Update Awair > {uuid} > {len(result)}")
        for unique_id, entity in result.items():
            target_domain = entity.get(DEVICE_DOMAIN)
            target_uuid = entity.get(DEVICE_ATTR).get("device_uuid")
            if not target_domain:
                self.log(0, f"Device domain does not exist > {unique_id} > {entity}")
                continue
            if target_uuid == uuid:
                self.init_device(unique_id, target_domain, entity)
                self.update_entity(unique_id, entity)

    async def update(self, event):
        """Update devices."""
        ip_list = []
        for info in self.awair.values():
            ip_list.append(info.get("ip"))
            await self.update_awair(info.get("device_uuid"))
        for addr in self.awair_list:
            if addr not in ip_list:
                setting = await self.get_setting(addr)
                uuid = setting.get("device_uuid")
                if uuid and not self.search_awair(uuid):
                    await self.add_awair(uuid, setting)
