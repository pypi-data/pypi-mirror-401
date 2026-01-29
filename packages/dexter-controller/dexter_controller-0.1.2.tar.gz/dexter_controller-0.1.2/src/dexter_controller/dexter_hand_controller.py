import threading
import time
from collections import defaultdict

from dexter_controller import Finger, FingerData, LoadCellDevice


class DexterHandController:
    def __init__(self, mapping):
        if not mapping:
            raise ValueError("mapping cannot be empty")

        self._mapping = dict(mapping)  # for reconnects
        self._lock = threading.Lock()

        self._finger_to_device = {}  # {Finger: (device, 0|1)}
        self._device_index_to_finger = {}  # {(device, 0|1): Finger}
        self._devices = []

        self.finger_data = defaultdict(lambda: FingerData([0, 0, 0, 0]))
        self._finger_has_data = defaultdict(bool)  # {Finger: bool}
        self._finger_last_update_ts = defaultdict(float)  # {Finger: float}

        self._callbacks = defaultdict(list)  # {Finger: [callback, ...]}
        self._stop_event = threading.Event()

        # Connection status
        self.available_ports = []
        self.unavailable_ports = []

        # Initial connect attempt (tolerates missing devices)
        self._connect_from_mapping(self._mapping)

        # Poll loop works in background thread
        self._poll_thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._poll_thread.start()

    def _connect_from_mapping(self, mapping):
        """
        Disconnect any existing devices and try to connect everything described by mapping.

        This is intentionally "reset + reconnect" to keep behavior simple and deterministic.
        """
        with self._lock:
            # Tear down existing connections
            for d in self._devices:
                try:
                    d.close()
                except Exception:
                    pass

            self._devices.clear()
            self._finger_to_device.clear()
            self._device_index_to_finger.clear()
            self.available_ports.clear()
            self.unavailable_ports.clear()

            # Reconnect all configured ports
            for com_port, fingers in mapping.items():
                try:
                    device = LoadCellDevice(com_port, start_thread=False)
                except Exception as e:
                    self.unavailable_ports.append(com_port)
                    print(f"Failed to connect to device on {com_port}: {e}")
                    continue

                self._devices.append(device)
                self.available_ports.append(com_port)

                # A LoadCellDevice yields two indices (0 and 1). Ignore extra configured fingers.
                if len(fingers) > 2:
                    print(
                        f"Warning: device {com_port} configured with {len(fingers)} fingers; "
                        "only the first two will be used (indices 0 and 1)."
                    )

                for i, finger in enumerate(fingers[:2]):
                    self._finger_to_device[finger] = (device, i)
                    self._device_index_to_finger[(device, i)] = finger

    def _poll_loop(self):
        while not self._stop_event.is_set():
            # Snapshot under lock to avoid races with reconnect()/close()
            with self._lock:
                devices = list(self._devices)
                device_index_to_finger = dict(self._device_index_to_finger)

            for device in devices:
                for event in device.get_events():
                    data = getattr(event, "payload", None)
                    if not data or len(data) < 8:
                        continue  # ignore malformed/partial events

                    # 8 values: 4 per index (0 and 1)
                    for i in (0, 1):
                        finger = device_index_to_finger.get((device, i))
                        if finger is None:
                            continue

                        finger_data = list(data[i * 4 : (i + 1) * 4])
                        self.finger_data[finger].raw_data = finger_data
                        self._finger_has_data[finger] = True
                        self._finger_last_update_ts[finger] = time.time()

                        for cb in self._callbacks[finger]:
                            cb(finger_data)

            time.sleep(0.001)

    def register_finger_callback(self, finger, callback):
        """Register a callback for a finger. Callback will be called with new data."""
        self._callbacks[finger].append(callback)

    def finger_has_data(self, finger):
        """True once we've received at least one payload for this finger."""
        return bool(self._finger_has_data[finger])

    def finger_last_update_ts(self, finger):
        """Unix timestamp (seconds) of last received payload for this finger; 0.0 if never."""
        return float(self._finger_last_update_ts[finger])

    def get_status(self):
        """
        Returns:
          - ports: {available: [...], unavailable: [...]}
          - fingers: {Finger: {has_data: bool, last_update_ts: float, mapped: bool}}
        """
        with self._lock:
            mapped_fingers = set(self._finger_to_device.keys())
            available_ports = list(self.available_ports)
            unavailable_ports = list(self.unavailable_ports)

        fingers_status = {}
        for f in (Finger.THUMB, Finger.INDEX, Finger.MIDDLE, Finger.RING, Finger.PINKY):
            fingers_status[f] = {
                "has_data": bool(self._finger_has_data[f]),
                "last_update_ts": float(self._finger_last_update_ts[f]),
                "mapped": f in mapped_fingers,
            }

        return {
            "ports": {"available": available_ports, "unavailable": unavailable_ports},
            "fingers": fingers_status,
        }

    def reconnect(self):
        """
        Disconnect any existing devices and try to reconnect everything from the original mapping.
        Returns: (available_ports, unavailable_ports)
        """
        self._connect_from_mapping(self._mapping)
        return list(self.available_ports), list(self.unavailable_ports)

    def close(self):
        self._stop_event.set()
        self._poll_thread.join()
        # Close all devices
        with self._lock:
            for device in self._devices:
                device.close()
            self._devices.clear()
            self._finger_to_device.clear()
            self._device_index_to_finger.clear()

        self._callbacks.clear()

    @property
    def thumb(self):
        return self.finger_data[Finger.THUMB]

    @property
    def index(self):
        return self.finger_data[Finger.INDEX]

    @property
    def middle(self):
        return self.finger_data[Finger.MIDDLE]

    @property
    def ring(self):
        return self.finger_data[Finger.RING]

    @property
    def pinky(self):
        return self.finger_data[Finger.PINKY]
