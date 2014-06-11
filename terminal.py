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
        self.params = {'alpha':1,'beta':1, 'Cmax':1}
    def objective_function(p):
        return self.params['alpha']*cvx.sum_squares(p)+self.params['beta']*sum_entries(p)
    def constrain(p):
        con = list()
        for i in range(1,len(p)):
            con.append(p[i+1,:]-p[i,:]<=self.params['Cmax'])
        return con
       
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
