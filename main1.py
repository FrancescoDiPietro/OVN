from random import shuffle
#from lab3 import Network, Connection
import matplotlib.pyplot as plt
from Net import Network, Connection


network = Network('nodes.json')
network.connect()
node_labels = list(network.nodes.keys())
connections = []
for i in range (100):
    shuffle(node_labels)
    connection = Connection(node_labels[0],node_labels[-1],1)
    connections.append(connection)

# streamed_connections = network.stream(connections)
# latencies=[connection.latency for connection in streamed_connections]
# plt.hist(latencies ,bins=10)
# plt.title('Latency Distribution')
# plt.show()

streamed_connections = network.stream(connections ,best='snr')
snrs = [connection.snr for connection in streamed_connections]
plt.hist(snrs,bins=10)
plt.title('SNR Distribution')
plt.show()