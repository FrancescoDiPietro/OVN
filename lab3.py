import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.constants import c


class SignalInformation(object):
    def __init__(self, power, path):
        self._signal_power = power
        self._path = path
        self._noise_power = 0
        self._latency = 0

    @property
    def signal_power(self):
        return self._signal_power

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def noise_power(self):
        return self._noise_power

    @noise_power.setter
    def noise_power(self, noise):
        self._noise_power = noise

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self, latency):
        self._latency = latency

    def add_noise(self, noise):
        self.noise_power += noise

    def add_latency(self, latency):
        self.latency += latency

    def next(self):
        self.path = self.path[1:]


class Node(object):
    def __init__(self, node_dict):
        self._label = node_dict['label']
        self._position = node_dict['position']
        self._connected_nodes = node_dict['connected_nodes']
        self._successive = {}

    @property
    def label(self):
        return self._label

    @property
    def position(self):
        return self._position

    @property
    def connected_nodes(self):
        return self._connected_nodes

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, successive):
        self._successive = successive

    def propagate(self, signal_information, occupation=False):
        path = signal_information.path

        if len(path) > 1:
            line_label = path[:2]  # Label to next Node for Line is created
            line = self.successive[line_label]  # Saves the NEXT node
            signal_information.next()  # Signal Path is Updated

            # Updates the signal_information propagating it,
            # then recursively sending it to the Line that then sends it to the
            # next node to collapse it all back in the end
            signal_information = line.propagate(signal_information, occupation)

        return signal_information


class Line(object):
    def __init__(self, line_dict):
        self._label = line_dict['label']
        self._length = line_dict['length']
        self._successive = {}
        self._state = 'free'

    @property
    def label(self):
        return self._label

    @property
    def state(self):
        return self._state

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._successive

    @state.setter
    def state(self,state):
        state = state.lower().strip()
        if state in ['free', 'occupied']:
            self._state = state
        else:
            print(f'ERROR: line state not recognized. Value: {state}')

    @successive.setter
    def successive(self, successive):
        self._successive = successive

    def latency_generation(self):
        latency = self.length / (c * 2 / 3)
        return latency

    def noise_generation(self, signal_power):
        noise = signal_power / (2 * self.length)
        return noise

    def propagate(self, signal_information, occupation=False):
        # Update latency
        latency = self.latency_generation()
        signal_information.add_latency(latency)

        # Update noise
        signal_power = signal_information.signal_power
        noise = self.noise_generation(signal_power)
        signal_information.add_noise(noise)

        # Update line state
        if occupation:
            self._state = 'occupied'

        node = self.successive[signal_information.path[0]]  # Finds next Node
        signal_information = node.propagate(signal_information, occupation)  # Sends the updated Signal to the next Node
        return signal_information  # Returns the Signal that has previously been recursively send forward


class Network(object):
    def __init__(self, json_path):
        node_json = json.load(open(json_path, 'r'))  # Load Json nodes file
        self._nodes = {}
        self._lines = {}
        self._weighted_paths = None
        self._connected = False

        for node_label in node_json:
            # Create the node instance
            node_dict = node_json[node_label]  # Saves the node dictionary in node_dict
            # for ex: {'connected_nodes': ['B', 'C', 'D'], 'position': [-350000.0, 150000.0], 'label': 'A'} for node A

            node_dict['label'] = node_label  # Looks useless the label is already there ?????????
            node = Node(node_dict)  # Creates the object Node for the single nodes
            self._nodes[node_label] = node  # Adds the node Object to the dictionary

            # Create the line instances
            for connected_node_label in node_dict['connected_nodes']:  # Iterates through all connected nodes
                line_dict = {}  # Temp dict to then add to the main dict
                line_label = node_label + connected_node_label  # Creates the label for the line
                line_dict['label'] = line_label  # Adds the label as an attribute
                node_position = np.array(node_json[node_label]['position'])  # Gets node position
                connected_node_position = np.array(
                    node_json[connected_node_label]['position'])  # Gets connected node position

                # Calculates distance of two points
                line_dict['length'] = np.sqrt(np.sum((node_position - connected_node_position) ** 2))
                line = Line(line_dict) # Creates the line object
                self._lines[line_label] = line # Adds the object to the dictionary

    @property
    def weighted_paths(self):
        return self._weighted_paths

    @property
    def connected(self):
        return self._connected

    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    def draw(self):
        nodes = self.nodes
        for node_label in nodes:
            n0 = nodes[node_label]
            x0 = n0.position[0]
            y0 = n0.position[1]
            plt.plot(x0, y0,'go', markersize = 10)
            plt.text(x0 + 30, y0 + 30, node_label)
            for connected_node_label in n0.connected_nodes:
                n1 = nodes[connected_node_label]
                x1 = n1.position[0]
                y1 = n1.position[1]
                plt.plot([x0, x1], [y0, y1],'b')
        plt.title('Network')
        plt.show()

    def propagate(self, signal_information):
        path = signal_information.path
        start_node = self.nodes[path[0]]
        propagated_signal_information = start_node.propagate(signal_information)
        return propagated_signal_information

    def connect(self):
        nodes_dict = self.nodes
        lines_dict = self.lines

        for node_label in nodes_dict:
            node = nodes_dict[node_label]
            for connected_node in node.connected_nodes:
                line_label = node_label + connected_node
                line = lines_dict[line_label]
                line.successive[connected_node] = nodes_dict[connected_node]
                node.successive[line_label] = lines_dict[line_label]
        self._connected = True

    def find_paths(self, label1, label2):
        cross_nodes = [key for key in self.nodes.keys() if ((key != label1) & (key != label2))]
        cross_lines = self.lines.keys()
        inner_paths = {}
        inner_paths['0'] = label1
        for i in range(len(cross_nodes) + 1):
            inner_paths[str(i + 1)] = []
            for inner_path in inner_paths[str(i)]:
                inner_paths[str(i+1)] += [inner_path + cross_node
                for cross_node in cross_nodes
                    if ((inner_path[-1]+cross_node in cross_lines) &
                        (cross_node not in inner_path))]
        paths = []
        for i in range(len(cross_nodes) + 1):
            for path in inner_paths[str(i)]:
                if path[-1] + label2 in cross_lines:
                    paths.append(path + label2)
        return paths

    def available_paths(self, input_node, output_node):
        if self._weighted_paths is None:
            self.weighted_paths(1)

        all_paths = [path for path in self.weighted_paths.path.values
                     if ((path[0] == input_node) and (path[-1] == output_node))]
        unavailable_lines = [line for line in self.lines if self.lines[line].state == 'occupied']
        available_paths = []
        for path in all_paths:
            available = True
            for line in unavailable_lines:
                if line[0] + '->' + line[1] in path:
                    available = False
                    break
        if available:
            available_paths.append(path)

        return available_paths

    def set_weighted_paths(self,signal_power):
        if not self.connected:
            self.connect()
        node_labels = self.nodes.keys()
        pairs = []
        for label1 in node_labels:
            for label2 in node_labels:
                if label1 != label2: pairs.append(label1 + label2)
        columns = ['path', 'latency', 'noise', 'snr']
        df = pd.DataFrame()
        paths = []
        latencies = []
        noises = []
        snrs = []
        for pair in pairs:
            for path in self.find_paths(pair[0], pair[1]):
                path_string = ''
                for node in path:
                    path_string += node + '->'
                paths.append(path_string[:-2])
                # Propagation
                signal_information = SignalInformation(signal_power, path)
                signal_information = self.propagate(signal_information)
                latencies.append(signal_information.latency)
                noises.append(signal_information.noise_power)
                snrs.append(10 * np.log10(signal_information.signal_power / signal_information.noise_power))

        df['path'] = paths
        df['latency'] = latencies
        df['noise'] = noises
        df['snr'] = snrs
        self._weighted_paths = df

    def find_best_snr(self, input_node, output_node):
        available_paths = self.available_paths(input_node, output_node)
        if available_paths:
            inout_df = self.weighted_paths.loc[self.weighted_paths.path.isin(available_paths)]
            best_snr = np.max(inout_df.snr.values)
            best_path = inout_df.loc[inout_df.snr == best_snr].path.values[0].replace('->', '')
            return best_path
        else:
            best_path = None
            return best_path

    def find_best_latency(self, input_node, output_node):
        available_paths = self.available_paths(input_node, output_node)
        if available_paths:
            inout_df = self.weighted_paths.loc[self.weighted_paths.path.isin(available_paths)]
            best_latency = np.min(inout_df.latency.values)
            best_path = inout_df.loc[inout_df.latency == best_latency].path.values[0].replace('->', '')
            return best_path
        else:
            best_paths = None
            return best_paths

    def stream(self, connections, best='latency'):
        streamed_connections = []
        for connection in connections:
            input_node = connection.input_node
            output_node = connection.output_node
            signal_power = connection.signal_power
            self.set_weighted_paths(signal_power)
            if best == 'latency':
                path = self.find_best_latency(input_node, output_node)
            elif best == 'snr':
                path = self.find_best_snr(input_node, output_node)
            else:
                print('ERROR: best input not recognized.Value:', best)
                continue
            if path: # in case path is None
                in_signal_information = SignalInformation(signal_power, path)
                out_signal_information = self.propagate(in_signal_information)
                connection.latency = out_signal_information.latency
                noise = out_signal_information.noise_power
                connection.snr = 10 * np.log10(signal_power / noise)
                streamed_connections.append(connection)
            else:
                connection.latency = None
                connection.snr = 0
                streamed_connections.append(connection)
        return streamed_connections


class Connection:
    def __init__(self,input_node,output_node,signal_power):
        self._input_node = input_node
        self._output_node = output_node
        self._signal_power = signal_power
        self._latency = 0
        self._snr = 0

    @property
    def input_node(self):
        return self._input_node

    @property
    def output_node(self):
        return self._output_node

    @property
    def signal_power(self):
        return self._signal_power

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self,latency):
        self._latency = latency

    @property
    def snr(self):
        return self._snr

    @snr.setter
    def snr(self,snr):
        self._snr = snr


def create_dataframe(): # point 5
    network = Network('nodes.json')
    network.connect()
    node_labels = network.nodes.keys()
    pairs = []
    for label1 in node_labels:
        for label2 in node_labels:
            if label1 != label2: pairs.append(label1 + label2)
    columns = ['path', 'latency', 'noise', 'snr']
    df = pd.DataFrame()
    paths = []
    latencies = []
    noises = []
    snrs = []
    for pair in pairs:
        for path in network.find_paths(pair[0], pair[1]):
            path_string = ''
            for node in path:
                path_string += node + '->'
            paths.append(path_string[:-2])
            # Propagation
            signal_information = SignalInformation(1, path)
            signal_information = network.propagate(signal_information)
            latencies.append(signal_information.latency)
            noises.append(signal_information.noise_power)
            snrs.append(10 * np.log10(signal_information.signal_power / signal_information.noise_power))

    df['path'] = paths
    df['latency'] = latencies
    df['noise'] = noises
    df['snr'] = snrs
    print(df.to_string())
    network.draw()


if __name__ == "__main__":
    net = Network('nodes.json')
    net.draw()
    # print(net.find_best_snr('A','D'))
