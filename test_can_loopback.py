"""
CAN message send receive

Scope:
Loopback Virtual Simulation using local software channel
Send and Receive CAN frame on same channel - using 2 virtual nodes

"""
from time import sleep
import can

# Loopback Virtual Simulation using local software channel
# Send and Receive CAN frame on same channel - using 2 virtual nodes

# Initialize
bus_sender = can.interface.Bus('sim_channel', interface='virtual')
bus_receiver = can.interface.Bus('sim_channel', interface='virtual')

# Define CAN frame (with 8 bytes of data)
tx_msg = can.Message(
    arbitration_id=0x123,
    data=[10, 20, 30, 40, 50, 60, 70, 80],
    is_extended_id=False
)

# Send CAN frame
print(f"Sending: {tx_msg}")
bus_sender.send(tx_msg)
#
sleep(0.1)
print("...done\n")

# Receive CAN message
rx_msg = bus_receiver.recv(timeout=0.1)

if rx_msg:
    print(f"Received CAN frame: {rx_msg}\n")
    print(f"Data Bytes: {list(rx_msg.data)}\n")
else:
    print("Timeout: No message received.")

# Cleanup
bus_sender.shutdown()
bus_receiver.shutdown()

