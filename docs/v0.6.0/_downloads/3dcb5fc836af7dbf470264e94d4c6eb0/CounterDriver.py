"""Software-only Open driver implementing the 0.6.0 contract without NeQOS imports."""

import asyncio
from copy import deepcopy
import math
import time


class CounterDriver:
    NEQOS_DEVICE_DRIVER_API_VERSION = "0.6.0"

    def __init__(self, deviceId, hardwareConfig=None):
        self.deviceId = deviceId
        config = dict(hardwareConfig or {})
        if set(config) - {"initialValue"}:
            raise ValueError("CounterDriver only supports hardwareConfig.initialValue")
        self._value = self._integer(config.get("initialValue", 0))
        self._connected = False
        self._initialized = False
        self._ready = False
        self._reason = "Not connected"
        self.driverIOLock = asyncio.Lock()
        self._taskRegistry = {
            "Increment": {
                "taskClass": "foreground",
                "admissionPolicy": "sync",
                "pausable": False,
                "description": "Increment a software counter and return the new value.",
                "resultSchema": {
                    "status": {
                        "type": "str", "required": True, "values": ["OK"],
                        "description": "Task outcome.",
                    },
                    "value": {
                        "type": "int", "required": True,
                        "description": "Counter after incrementing.",
                    },
                },
            }
        }

    @staticmethod
    def _integer(value):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("Counter values must be integers, not booleans")
        return value

    async def Connect(self):
        self._connected = True
        self._reason = "Connected; initialization required"
        return True

    async def Disconnect(self):
        self._ready = self._initialized = self._connected = False
        self._reason = "Disconnected"
        return True

    async def Initialize(self):
        if not self._connected:
            raise RuntimeError("Connect before Initialize")
        self._initialized = True
        self._reason = "Initialized; readiness required"
        return True

    async def RecoverTransport(self):
        await self.Disconnect()
        await self.Connect()
        return {"status": "OK", "connected": True, "initialized": False, "ready": False}

    async def SetReady(self):
        if not (self._connected and self._initialized):
            raise RuntimeError("Connected and initialized state required")
        self._ready = True
        self._reason = "Ready"
        return True

    async def ClearReady(self):
        self._ready = False
        self._reason = "Not ready"
        return True

    async def ProbeConnection(self):
        return self._connected

    async def ReadTelemetry(self):
        return {"parameters": {"value": self._value}, "signals": {},
                "status": self.BuildStateSnapshot(), "timestamp": time.time()}

    async def SetParameter(self, name, value, *, timeoutSec=None):
        if name != "value":
            raise ValueError(f"Unknown parameter {name!r}")
        value = self._integer(value)
        async with self.driverIOLock:
            self._value = value
        return self._value

    async def GetParameter(self, name, *, timeoutSec=None):
        if name != "value":
            raise ValueError(f"Unknown parameter {name!r}")
        return self._value

    async def ReadSignal(self, name, *, timeoutSec=None):
        raise ValueError(f"No signals declared: {name!r}")

    async def EmergencyAbortIO(self):
        # Software-only: no blocking transport to interrupt.
        return None

    def GetCapabilities(self):
        return {"parameters": {"value": {"type": "int", "default": self._value,
                    "description": "Current counter value."}}, "signals": {},
                "commands": ["INITIALIZE", "SET_READY", "CLEAR_READY", "DISCONNECT"],
                "foregroundTasks": deepcopy(self._taskRegistry), "backgroundTasks": {}}

    def BuildStateSnapshot(self):
        return {"connected": self._connected, "initialized": self._initialized,
                "ready": self._ready, "reason": self._reason, "timestamp": time.time()}

    def IsIOBusy(self):
        return self.driverIOLock.locked()

    def GetConnectionProbeTimeoutSec(self):
        return 1.0

    async def Increment(self, amount: int = 1, durationSec: float = 0.0, context=None):
        """Wait cooperatively, then increment the counter.

        Args:
            amount: Signed integer added to the counter.
            durationSec: Non-negative software delay in seconds.
        """
        if not self._ready:
            raise RuntimeError("Counter is not ready")
        amount = self._integer(amount)
        duration = float(durationSec)
        if not math.isfinite(duration) or duration < 0:
            raise ValueError("durationSec must be finite and non-negative")
        deadline = time.monotonic() + duration
        async with self.driverIOLock:
            while True:
                if context is not None and context.cancelled:
                    return {"status": "CANCELLED", "reason": context.reason}
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    break
                await asyncio.sleep(min(remaining, 0.01))
            self._value += amount
            return {"status": "OK", "value": self._value}
