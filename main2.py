from random import shuffle
import matplotlib.pyplot as plt
import numpy as np
from Net import Network, Connection

# Full Fixed
network = Network('247000.json')
network.connect()
node_labels = list(network.nodes.keys())
connections = []
for i in range(100):
    shuffle(node_labels)
    connection = Connection(node_labels[0],node_labels[-1],1)
    connections.append(connection)

streamed_connections = network.stream(connections, best='snr')

bit_rate_fixed_rate = [connection.bit_rate for connection in streamed_connections]
#brfr = np.ma.masked_equal(bit_rate_fixed_rate, 0)

plt.hist(bit_rate_fixed_rate, label='fixed-rate')
plt.title('BitRate Full fixed-rate')
plt.xlabel('Gbps')
plt.show()


# Full Flex
network = Network('nodes_full_flex_rate.json')
network.connect()
node_labels = list(network.nodes.keys())
connections = []
for i in range (100):
    shuffle(node_labels)
    connection = Connection(node_labels[0],node_labels[-1],1)
    connections.append(connection)

streamed_connections = network.stream(connections ,best='snr')

bit_rate_flexed_rate = [connection.bit_rate for connection in streamed_connections]
#brfr = np.ma.masked_equal(bit_rate_flexed_rate, 0)

plt.hist(bit_rate_flexed_rate, label='flex-rate')
plt.title('BitRate Full flex-rate')
plt.xlabel('Gbps')
plt.show()


# Full Shannon
network = Network('nodes_full_shannon.json')
network.connect()
node_labels = list(network.nodes.keys())
connections = []
for i in range (100):
    shuffle(node_labels)
    connection = Connection(node_labels[0],node_labels[-1],1)
    connections.append(connection)

streamed_connections = network.stream(connections ,best='snr')

bit_rate_shannon_rate = [connection.bit_rate for connection in streamed_connections]
#brfr = np.ma.masked_equal(bit_rate_shannon_rate, 0)

plt.hist(bit_rate_shannon_rate, label='shannon-rate')
plt.title('BitRate Full shannon-rate')
plt.xlabel('Gbps')
plt.show()