## IoT ESP32 MQTT Demo (Wokwi)

An ESP32 IoT demo using MicroPython and MQTT on Wokwi. It publishes gas and motion sensor data and subscribes to commands to control a white LED and an RGB LED.

### Features
- **Sensors**: Gas sensor (analog), PIR motion sensor.
- **Actuators**: White LED, RGB LED (common anode).
- **MQTT**: Publishes sensor telemetry and subscribes to control topics.
- **Simulation**: Fully runnable on Wokwi with provided `diagram.json`.

### Hardware Mapping (per `project/diagram.json`)
- **ESP32 board**: `board-esp32-devkit-c-v4`
- **White LED**: `GPIO4`
- **RGB LED (common anode)**: `R=GPIO16`, `G=GPIO17`, `B=GPIO18`, `COM=3V3`
- **Gas sensor**: `AOUT -> GPIO34`, `VCC -> 3V3`, `GND -> GND`
- **PIR sensor**: `OUT -> GPIO19`, `VCC -> 3V3`, `GND -> GND`

## Topic Tree

Broker: `test.mosquitto.org` (public test broker)

Root namespace used in code: `sachin`

```
sachin
├─ led1    # Subscribe: control white LED; payload: "on" | "off"
├─ rgb     # Subscribe: control RGB LED; payload: "red" | "green" | "blue" | "off"
└─ sensor  # Publish: JSON telemetry { gas, motion, timestamp }
```

Example telemetry payload published to `sachin/sensor`:

```json
{ "gas": 1234, "motion": 0, "timestamp": 1690000000.0 }
```

## MQTT Broker Commands

Using Mosquitto CLI tools.

Subscribe to all topics under `sachin/`:

```bash
mosquitto_sub -h test.mosquitto.org -t "sachin/#"
```

Control the white LED:

```bash
# Turn ON
mosquitto_pub -h test.mosquitto.org -t sachin/led1 -m "on"

# Turn OFF
mosquitto_pub -h test.mosquitto.org -t sachin/led1 -m "off"
```

Control the RGB LED:

```bash
mosquitto_pub -h test.mosquitto.org -t sachin/rgb -m "red"
mosquitto_pub -h test.mosquitto.org -t sachin/rgb -m "green"
mosquitto_pub -h test.mosquitto.org -t sachin/rgb -m "blue"
mosquitto_pub -h test.mosquitto.org -t sachin/rgb -m "off"
```

Listen specifically to sensor telemetry:

```bash
mosquitto_sub -h test.mosquitto.org -t "sachin/sensor"
```

## Run on Wokwi

Two ways to run:

- **From Wokwi site**: The project file `project/wokwi-project.txt` indicates a new ESP32 project. Upload the following into Wokwi:
  - `project/diagram.json`
  - `project/main.py` (as MicroPython main)
  - Ensure board is ESP32 and Internet is enabled (Wokwi-GUEST)

- **Locally in Wokwi CLI** (optional):
  1. Install Wokwi CLI and set up your environment.
  2. Place `diagram.json` and `main.py` as above.
  3. Start the simulation; serial monitor will show WiFi and MQTT logs.

MicroPython script behavior (`project/main.py`):
- Connects to WiFi SSID `Wokwi-GUEST` (empty password).
- Connects to MQTT broker `test.mosquitto.org` with client id `sachin`.
- Subscribes to `sachin/led1`, `sachin/rgb`.
- Publishes telemetry to `sachin/sensor` every 5 seconds.

## Files

- `project/main.py`: MicroPython logic (WiFi, MQTT, sensor read, LED control).
- `project/diagram.json`: Wokwi wiring and board configuration.
- `project/wokwi-project.txt`: Wokwi project metadata.
## Sceenshots
<img width="923" height="741" alt="Screenshot 2025-10-28 at 10 49 05ΓÇ»PM" src="https://github.com/user-attachments/assets/a9804311-b6ad-4972-8711-60bace718bd8" />
<img width="737" height="917" alt="Screenshot 2025-10-28 at 10 54 32ΓÇ»PM" src="https://github.com/user-attachments/assets/51127d17-e09f-46da-b936-2133d2f44bdf" />
<img width="1326" height="648" alt="Screenshot 2025-10-28 at 10 55 15ΓÇ»PM" src="https://github.com/user-attachments/assets/70f3f299-fbfb-43f0-b257-4f3eef848fd3" />
<img width="923" height="741" alt="Screenshot 2025-10-28 at 10 49 38ΓÇ»PM" src="https://github.com/user-attachments/assets/7e43a13f-3921-427f-9674-f517d91ce4bb" />
<img width="923" height="741" alt="Screenshot 2025-10-28 at 10 50 25ΓÇ»PM" src="https://github.com/user-attachments/assets/aa578057-076c-4051-acd8-da4acc61376e" />
<img width="923" height="741" alt="Screenshot 2025-10-28 at 10 51 09ΓÇ»PM" src="https://github.com/user-attachments/assets/f7e10e9c-3a87-4ef0-89f7-92f696cd293a" />

<img width="737" height="917" alt="Screenshot 2025-10-28 at 10 54 21ΓÇ»PM" src="https://github.com/user-attachments/assets/13acb3cf-8b80-4463-9bf4-c088e0148eba" />

