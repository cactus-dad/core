"""The ext router integration."""

from __future__ import annotations

from homeassistant.components import mqtt
from homeassistant.components.mqtt import ReceiveMessage
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "ext_router"
CONF_TOPIC = "topic"
DEFAULT_TOPIC = "ha/test"


def _payload_to_string(payload) -> str:
    if isinstance(payload, (bytes, bytearray, memoryview)):
        payload = bytes(payload)
        return payload.decode("utf-8", errors="replace")
    return payload


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the MQTT component."""
    topic = config[DOMAIN][CONF_TOPIC]
    entity_id = "ext_router.test_message"

    def message_received(msg: ReceiveMessage) -> None:
        """Handle a new MQTT message."""
        hass.states.set(entity_id, _payload_to_string(msg.payload))

    mqtt.subscribe(hass, topic, message_received)
    hass.states.set(entity_id, "waiting for mqtt")
    return True
