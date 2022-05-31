from scipy.constants import c


class Line(object):
    def __init__(self, line_dict):
        self._label = line_dict['label']
        self._length = line_dict['length']
        self._successive = {}
        self._state = ['free']*10

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
        state = [s.lower().strip() for s in state]
        if set(state).issubset(['free', 'occupied']):
            self._state = state
        else:
            print('ERROR: line state not recognized. Value:', set(state) - set(['free', 'occupied']))

    @successive.setter
    def successive(self, successive):
        self._successive = successive

    def latency_generation(self):
        latency = self.length / (c * 2 / 3)
        return latency

    def noise_generation(self, signal_power):
        noise = signal_power / (2 * self.length)
        return noise

    def propagate(self, lightpath, occupation=False):
        # Update latency
        latency = self.latency_generation()
        lightpath.add_latency(latency)

        # Update noise
        signal_power = lightpath.signal_power
        noise = self.noise_generation(signal_power)
        lightpath.add_noise(noise)

        # Update line state
        if occupation:
            channel = lightpath.channel
            new_state = self.state.copy()
            new_state[channel] = 'occupied'
            self.state = new_state

        node = self.successive[lightpath.path[0]]  # Finds next Node
        lightpath = node.propagate(lightpath, occupation)  # Sends the updated Signal to the next Node
        return lightpath  # Returns the Signal that has previously been recursively send forward

    def probe(self, signal_information):
        # Update latency
        latency = self.latency_generation()
        signal_information.add_latency(latency)

        # Update noise
        signal_power = signal_information.signal_power
        noise = self.noise_generation(signal_power)
        signal_information.add_noise(noise)

        node = self.successive[signal_information.path[0]]  # Finds next Node
        signal_information = node.probe(signal_information)  # Sends the updated Signal to the next Node
        return signal_information  # Returns the Signal that has previously been recursively send forward
