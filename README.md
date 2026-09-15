Working with Virtual Nodes, software channel, and DBC files for ECU CAN testing.

Usage:
# Test CAN frame tx and rx using 2 virtual nodes on a software channel
python test_can_loopback.py
# Test ECU Simulation using cantools for loading DBC file
python test_can_ecu.py <.dbc filename>