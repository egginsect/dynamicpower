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
        self.T = 10 
        self.p = 0 

class Generator(Device):
    def __init__(self, name, connections):
        Device.__init__(self, name, 'G', connections)
        self.params = {'alpha':1,'beta':1, 'Cmax':1}
    def cost_function(self,p):
        return self.params['alpha']*cvx.sum_squares(p)+self.params['beta']*cvx.sum_entries(p)
    def constrain(self,p):
        con = list()
        for i in range(1, p.size[0]):
            con.append(p[i,:]-p[i-1,:]<=self.params['Cmax'])
        return con
    def solve_problem(self,u):
        p = cvx.Variable(self.T)
        objective = cvx.Minimize(self.cost_function(p))
        constraints = self.constrain(p)
        prob = cvx.Problem(objective, constraints)
        prob.solve()
        self.p = p.value   
        print np.mean(p.value)
    def compute_cost(self):
        p = self.solve_problem(2)
        print 'Compute cost for Geenerator',self.name
        print np.mean(p)
        return np.mean(self.p) 
       
class Battery(Device):
    def __init__(self, name, connections):
        Device.__init__(self, name, 'B', connections)
    def compute_cost(self):
        return np.mean(self.p) 
        
class TransmissionLine(Device):
    def __init__(self, name, connections):
        Device.__init__(self, name, 'T', connections)
    def compute_cost(self):
        return np.mean(self.p) 

class DefferableLoad(Device):
    def __init__(self, name, connections):
        Device.__init__(self, name, 'DL', connections)
    def compute_cost(self):
        return np.mean(self.p) 

class CurtalibleLoad(Device):
    def __init__(self, name, connections):
        Device.__init__(self, name, 'CL', connections)
    def compute_cost(self):
        return np.mean(self.p) 
