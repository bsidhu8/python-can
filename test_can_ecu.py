"""
CAN message send receive

Scope:
ECU Simulation - DBC File Decoding and Cyclic Messages

Steps:
    - Create a DBC file
    - Load DBC file
    - Create 2 Virtual Nodes using a local software channel
    - encode message
    - transmit message
    - receive message
    - decode message

DBC (Database CAN) lists -
    - which ECU (Nodes) transmits or recieves specific messages
    - translates hex data into human readable 60km/h
    - details of signal parameters used for conversion
    BU_ Nodes - which ECUs are connected to the network
    BO_ Messages - CAN message IDs, names
    SG_ Signals  - scaling and units for data payload in CAN messages
DBC files used in HITL and SITL for ECU testing and validation

"""
import sys
import can
import cantools
from time import sleep

# DBC file to use
try:
    if ".dbc" in sys.argv[1]:
        dbc_file = sys.argv[1]
except:
    dbc_file = "vehicle_database.dbc"

# Load DBC file
db = cantools.database.load_file(dbc_file)

# Create 2 Virtual Nodes
ecu_bus = can.interface.Bus("vehicle_network", interface="virtual")
monitor_bus = can.interface.Bus("vehicle_network", interface="virtual")
print("Virtual Nodes created")
print("ECU Simulator active...")

# Simulated vehicle states
current_rpm = 800
current_temp = 20
current_oiltemp = 30

try:
    for _ in range(5): # Simulate 5 consequetive broadcast steps

        # Update simulated data metrics dynamically
        current_rpm += 150
        current_temp += 1
        current_oiltemp += 5

        # Encode physical vaules > raw data w.r.t. DBC file
        raw_data = db.encode_message("EngineStatus",
                    {'EngineRPM': current_rpm,
                     'CoolantTemperature': current_temp,
                     'OilTemperature': current_oiltemp})

        # Build CAN message
        # Extract CAN message arbitration parameters from DBC file
        msg_definition = db.get_message_by_name("EngineStatus")
        # build CAN frame
        tx_frame = can.Message(
            arbitration_id=msg_definition.frame_id,
            data=raw_data,
            is_extended_id=False
        )

        # Transmit CAN frame
        ecu_bus.send(tx_frame)
        print(f"[TX Node] Current physical states: {current_rpm} RPM {current_temp} C\n")

        # Receive CAN frame
        rx_frame = monitor_bus.recv(timeout=0.5)

        # Decode CAN frame
        if rx_frame:
            decoded_metrics = db.decode_message(
                rx_frame.arbitration_id,
                rx_frame.data
            )
            print(f"[RX Node] Decoded frame: {decoded_metrics}\n")

            #
            sleep(1.0) # stream interval spacing

finally:
    ecu_bus.shutdown()
    monitor_bus.shutdown()
    print("Simulation terminated")