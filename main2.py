from random import shuffle
import matplotlib.pyplot as plt
import numpy as np
from Net import Network, Connection

network_flexed = Network('247000_full_flex.json')
network_fixed = Network('247000_full_fixed.json')
network_shannon = Network('247000_full_shannon.json')

network_fixed.connect()

network_fixed.draw()

node_labels_fixed = list(network_fixed.nodes.keys())
connections = []
# --------------------------------------------------------------------------------------------------
su_connections = []

for i in range(100):
    shuffle(node_labels_fixed)
    connection = Connection(node_labels_fixed[0], node_labels_fixed[-1], 1)
    connections.append(connection)

for j in range(100):
    network_fixed.traffic_matrix = network_fixed.create_traffic_matrix(j + 1)
    network_fixed.stream2(connections, best='snr')
    print(j)
    su_connections.append(network_fixed.suc_connections)
    if network_fixed.suc_connections == 100:
        break

plt.plot(su_connections)
plt.title('Saturation Fixed Rate')
plt.xlabel('M')
plt.ylabel('number of saturated requests')
plt.show()

# --------------------------------------------------------------------------------------------------

# print(su_connections)
#
# network_flexed.connect()
# network_shannon.connect()
#
# network_fixed.draw()
#
# for i in range(100):
#     shuffle(node_labels_fixed)
#     connection = Connection(node_labels_fixed[0],node_labels_fixed[-1],1)
#     connections.append(connection)
#
# # signal to Noise Ratio
# streamed_connections = network_fixed.stream(connections, best='snr')
#
# snrs = [connection.snr for connection in streamed_connections]
# snrs_ = np.ma.masked_equal(snrs, 0)
# plt.hist(snrs_, bins=20)
#
# plt.title('SNR Distribution')
# plt.xlabel('dB')
# plt.show()
#
# # Latency dist
# streamed_connections = network_fixed.stream(connections, best='snr')
#
# latencies = [connection.latency for connection in streamed_connections]
# plt.hist(np.ma.masked_equal(latencies, 0), bins=25)
#
# plt.title('Latency Distribution')
# plt.xlabel('ms')
# plt.show()
#
#
# # Full Fixed
#
# #network.draw()
# streamed_connections = network_fixed.stream(connections, best='snr')
#
# bit_rate_fixed_rate = [connection.bit_rate for connection in streamed_connections]
#
# plt.hist(bit_rate_fixed_rate, label='fixed-rate')
# plt.title('BitRate Full fixed-rate')
# plt.xlabel('Gbps')
# plt.show()
#
#
# # Full Flex
# node_labels_flex = list(network_flexed.nodes.keys())
# connections = []
# for i in range (100):
#     shuffle(node_labels_flex)
#     connection = Connection(node_labels_flex[0],node_labels_flex[-1],1)
#     connections.append(connection)
#
# streamed_connections = network_flexed.stream(connections, best='snr')
#
# bit_rate_flexed_rate = [connection.bit_rate for connection in streamed_connections]
#
# plt.hist(bit_rate_flexed_rate, label='flex-rate')
# plt.title('BitRate Full flex-rate')
# plt.xlabel('Gbps')
# plt.show()
#
#
# # Full Shannon
# node_labels_shannon = list(network_shannon.nodes.keys())
# connections = []
# for i in range (100):
#     shuffle(node_labels_shannon)
#     connection = Connection(node_labels_shannon[0],node_labels_shannon[-1],1)
#     connections.append(connection)
#
# streamed_connections = network_shannon.stream(connections ,best='snr')
#
# bit_rate_shannon_rate = [connection.bit_rate for connection in streamed_connections]
#
# plt.hist(bit_rate_shannon_rate, label='shannon-rate')
# plt.title('BitRate Full shannon-rate')
# plt.xlabel('Gbps')
# plt.show()