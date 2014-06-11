import numpy as np
from proximal import *
class Terminal(object):
    def __init__(self, name, terminal_type, connections):
        self.name = name
        self.terminal_type = terminal_type

class Net(Terminal):
    def __init__(self, name, connections):
        Terminal.__init__(self, name, 'Net', connections)

class Device(Terminal):
    def __init__(self, name, device_type, connections):
        Terminal.__init__(self, name, 'Device', connections)
        self.device_type = device_type

class Generator(Device):
    def __init__(self, name, connections):
        Device.__init__(self, name, 'G', connections)
       
class Battery(Device):
    def __init__(self, name, connections):
        Device.__init__(self, name, 'B', connections)
        
class TransmissionLine(Device):
    def __init__(self, name, connections):
        Device.__init__(self, name, 'T', connections)

class DefferableLoad(Device):
    def __init__(self, name, connections):
        Device.__init__(self, name, 'DL', connections)

class CurtalibleLoad(Device):
    def __init__(self, name, connections):
        Device.__init__(self, name, 'CL', connections)
