import numpy as np
from threading import Thread
from proximal import *
class Terminal(Thread):
    def __init__(self, name, terminal_type, connections, params = None):
        Thread.__init__(self)
        self.name = name
        self.terminal_type = terminal_type
        self.T = 10 
        self.pbar = 1
        self.u = np.random.uniform(size=(10,1))
        self.params = params

 
class Net(Terminal):
    def __init__(self, name, connections, params = None):
        Terminal.__init__(self, name, 'Net', connections, params)
        self.params = params
        self.power_buffer = [np.zeros([self.T,1])]*len(connections)
        self.power_imbalance = None

class Device(Terminal):
    def __init__(self, name, device_type, connections, params):
        Terminal.__init__(self, name, 'Device', connections, params)
        self.device_type = device_type
        self.p = 0 
    def run(self):
            print self.name, 'is running'

class Generator(Device):
    def __init__(self, name, connections, params={'alpha':1,'beta':1, 'Cmax':1}):
        Device.__init__(self, name, 'G', connections, params)

class Battery(Device):
    def __init__(self, name, connections, params=None):
        Device.__init__(self, name, 'B', connections, params)
