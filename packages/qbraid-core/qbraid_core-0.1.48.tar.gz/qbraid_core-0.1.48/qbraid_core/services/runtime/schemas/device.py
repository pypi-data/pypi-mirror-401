# Copyright (c) 2025, qBraid Development Team
# All rights reserved.

"""
Pydantic schemas for device API responses.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, field_serializer

from qbraid_core.decimal import Credits

from .enums import DeviceStatus, ExperimentType


class DevicePricing(BaseModel):
    """Represents pricing information for a quantum device."""

    model_config = ConfigDict(frozen=True)

    perTask: Credits
    perShot: Credits
    perMinute: Credits

    @field_serializer("perTask", "perShot", "perMinute")
    def serialize_credits(self, value: Credits) -> float:
        """Serialize Credits objects to float for JSON response."""
        return float(value)


class RuntimeDevice(BaseModel):
    """Schema for device response"""

    name: str
    qrn: str
    vendor: Literal["aws", "azure", "ibm", "ionq", "qbraid"]
    deviceType: Literal["SIMULATOR", "QPU"]
    runInputTypes: list[str]
    status: DeviceStatus
    statusMsg: Optional[str] = None
    nextAvailable: Optional[datetime] = None
    queueDepth: Optional[int] = None
    avgQueueTime: Optional[int] = None  # in minutes
    numberQubits: Optional[int] = None
    paradigm: ExperimentType
    modality: Optional[str] = None  # only applies to QPUs
    noiseModels: Optional[list[str]] = None  # only applies to simulators
    pricingModel: Optional[Literal["fixed", "dynamic"]] = None  # None if direct access is False
    pricing: Optional[DevicePricing] = None  # only applies to fixed pricing model
    directAccess: bool = True
