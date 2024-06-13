"""Entity base class."""

from __future__ import annotations

from typing import Generic

from typing_extensions import TypeVar
from wyzeapy.services.base_service import BaseService
from wyzeapy.types import Device

from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, DeviceInfo
from homeassistant.helpers.entity import Entity

from .const import DOMAIN

_DeviceT = TypeVar("_DeviceT", bound=Device)
_ServiceT = TypeVar("_ServiceT", bound=BaseService)


class WyzeDeviceEntity(Generic[_DeviceT, _ServiceT], Entity):
    """Wyze device entity."""

    _attr_should_poll = False

    def __init__(self, device: _DeviceT, service: _ServiceT) -> None:
        """Initialize the entity."""
        self._device = device
        self._service = service

        if mac := getattr(device, "parent_device_mac"):
            self._attr_device_info = DeviceInfo(
                connections={(CONNECTION_NETWORK_MAC, mac)},
                identifiers={(DOMAIN, mac)},
            )
        else:
            mac = device.mac
            self._attr_device_info = DeviceInfo(
                connections={(CONNECTION_NETWORK_MAC, mac)},
                identifiers={(DOMAIN, mac)},
                name=device.nickname,
                manufacturer="WyzeLabs",
                model=device.product_model,
                sw_version=getattr(device, "firmware_ver"),
            )

    @property
    def available(self):
        """Return True if entity is available.."""
        return self._device.available
