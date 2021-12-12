"""Constants for the Damda Wair integration."""
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_BILLION,
    CONCENTRATION_PARTS_PER_MILLION,
    LIGHT_LUX,
    PERCENTAGE,
    TEMP_CELSIUS,
    SOUND_PRESSURE_WEIGHTED_DBA,
)

VERSION = "1.2.3"
BRAND = "Damda"
NAME = "Damda Awair"
NAME_KOR = "담다 어웨어"
DOMAIN = "damda_awair"
MODEL = "damda_awair"
MANUFACTURER = "Awair"
API_NAME = DOMAIN + "_api"
API_DEVICE = DOMAIN + "_device"
PLATFORMS = [SENSOR_DOMAIN]

DEVICE_DOMAIN = "domain"
DEVICE_ENTITY = "entity"
DEVICE_UPDATE = "update"
DEVICE_REG = "register"
DEVICE_TRY = "try"
DEFAULT_AVAILABLE = "available"

DEVICE_ICON = "icon"
DEVICE_CLASS = "device_class"
DEVICE_UNIT = "unit_of_measurement"
DEVICE_ATTR = "attributes"
DEVICE_STATE = "state"
DEVICE_UNIQUE = "unique_id"
DEVICE_ID = "entity_id"
DEVICE_NAME = "entity_name"

SETTING_URL = "http://{}/settings/config/data"
DATA_URL = "http://{}/air-data/latest"

AWAIR_DEVICE = {
    "awair-r2": [
        "score",
        "temp",
        "humid",
        "co2",
        "voc",
        "pm25",
        "timestamp",
        "dew_point",
        "abs_humid",
        "co2_est",
        "co2_est_baseline",
        "voc_baseline",
        "voc_h2_raw",
        "voc_ethanol_raw",
        "pm10_est",
    ],
    "awair-mint": [
        "score",
        "temp",
        "humid",
        "voc",
        "pm25",
        "timestamp",
        "dew_point",
        "abs_humid",
        "voc_baseline",
        "voc_h2_raw",
        "voc_ethanol_raw",
        "pm10_est",
        "lux",
        "spl_a",
    ],
    "awair-omni": [
        "score",
        "temp",
        "humid",
        "co2",
        "voc",
        "pm25",
        "timestamp",
        "dew_point",
        "abs_humid",
        "co2_est",
        "co2_est_baseline",
        "voc_baseline",
        "voc_h2_raw",
        "voc_ethanol_raw",
        "pm10_est",
        "lux",
        "spl_a",
    ],
    "awair-element": [
        "score",
        "temp",
        "humid",
        "co2",
        "voc",
        "pm25",
        "timestamp",
        "dew_point",
        "abs_humid",
        "co2_est",
        "co2_est_baseline",
        "voc_baseline",
        "voc_h2_raw",
        "voc_ethanol_raw",
        "pm10_est",
    ],
}

AWAIR_ITEM = {
    "score": ["score", "점수", "", SENSOR_DOMAIN, "mdi:periodic-table", None, int],
    "temp": [
        "temperature",
        "온도",
        TEMP_CELSIUS,
        SENSOR_DOMAIN,
        "mdi:thermometer",
        SensorDeviceClass.TEMPERATURE,
        float,
    ],
    "humid": [
        "humidity",
        "습도",
        PERCENTAGE,
        SENSOR_DOMAIN,
        "mdi:water-percent",
        SensorDeviceClass.HUMIDITY,
        float,
    ],
    "co2": [
        "co2",
        "이산화탄소",
        CONCENTRATION_PARTS_PER_MILLION,
        SENSOR_DOMAIN,
        "mdi:molecule-co2",
        SensorDeviceClass.CO2,
        int,
    ],
    "voc": [
        "voc",
        "VOC",
        CONCENTRATION_PARTS_PER_BILLION,
        SENSOR_DOMAIN,
        "mdi:chemical-weapon",
        SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
        int,
    ],
    "pm25": [
        "pm25",
        "초미세먼지",
        CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        SENSOR_DOMAIN,
        "mdi:blur",
        SensorDeviceClass.PM25,
        int,
    ],
    "lux": [
        "lux",
        "조도",
        LIGHT_LUX,
        SENSOR_DOMAIN,
        "mdi:weather-sunny",
        SensorDeviceClass.ILLUMINANCE,
        int,
    ],
    "spl_a": [
        "noise",
        "소음",
        SOUND_PRESSURE_WEIGHTED_DBA,
        SENSOR_DOMAIN,
        "mdi:volume-vibrate",
        None,
        int,
    ],
    "timestamp": [
        "updatetime",
        "업데이트",
        None,
        SENSOR_DOMAIN,
        "mdi:clock-outline",
        SensorDeviceClass.TIMESTAMP,
        None,
    ],
    "dew_point": [
        "dew_point",
        "이슬점",
        TEMP_CELSIUS,
        SENSOR_DOMAIN,
        "mdi:snowflake",
        SensorDeviceClass.TEMPERATURE,
        float,
    ],
    "abs_humid": [
        "abs_humidity",
        "절대습도",
        "",
        SENSOR_DOMAIN,
        "mdi:water-percent",
        SensorDeviceClass.HUMIDITY,
        float,
    ],
    "co2_est": [
        "co2_est",
        "이산화탄소 추정치",
        CONCENTRATION_PARTS_PER_MILLION,
        SENSOR_DOMAIN,
        "mdi:molecule-co2",
        SensorDeviceClass.CO2,
        int,
    ],
    "co2_est_baseline": [
        "co2_est_baseline",
        "이산화탄소 추정치 Baseline",
        "",
        SENSOR_DOMAIN,
        "mdi:molecule-co2",
        SensorDeviceClass.CO2,
        int,
    ],
    "voc_baseline": [
        "voc_baseline",
        "VOC Baseline",
        "",
        SENSOR_DOMAIN,
        "mdi:chemical-weapon",
        SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
        int,
    ],
    "voc_h2_raw": [
        "voc_h2_raw",
        "VOC H2 Raw",
        "",
        SENSOR_DOMAIN,
        "mdi:chemical-weapon",
        SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
        int,
    ],
    "voc_ethanol_raw": [
        "voc_ethanol_raw",
        "VOC 에탄올 Raw",
        "",
        SENSOR_DOMAIN,
        "mdi:chemical-weapon",
        SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
        int,
    ],
    "pm10_est": [
        "pm10_est",
        "미세먼지",
        CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        SENSOR_DOMAIN,
        "mdi:blur",
        SensorDeviceClass.PM10,
        int,
    ],
}
