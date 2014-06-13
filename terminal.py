import numpy as np
from proximal import *
class Terminal(object):
    def __init__(self, name, terminal_type, connections):
        self.name = name
        self.terminal_type = terminal_type
        self.T = 10 
        self.pbar = 1
        self.u = np.random.uniform(size=(10,1))

class Net(Terminal):
    def __init__(self, name, connections):
        Terminal.__init__(self, name, 'Net', connections)
    def update_price(self):
        print self.name, 'update_price'

class Device(Terminal):
    def __init__(self, name, device_type, connections, params):
        Terminal.__init__(self, name, 'Device', connections)
        self.device_type = device_type
        self.params = params
        self.p = 0 
        self.lmbd = 1
       

    def cost_function(self, p):
        return prox_operator(self.fx, p, self.lmbd, self.u+self.pbar)

class Generator(Device):
    def __init__(self, name, connections, params={'alpha':1,'beta':1, 'Cmax':1}):
        Device.__init__(self, name, 'G', connections, params)
        
    def fx(self,p):
        return self.params['alpha']*cvx.sum_squares(p)+self.params['beta']*cvx.sum_entries(p)
    
    def constrains(self,p):
        con = list()
        for i in range(1, p.size[0]):
            con.append(p[i,:]-p[i-1,:]<=self.params['Cmax'])
        return con
        '''def solve_problem(self,u):
        p = cvx.Variable(self.T)
        objective = cvx.Minimize(self.cost_function(p))
        constraints = self.constrain(p)
        prob = cvx.Problem(objective, constraints)
        prob.solve()
        self.p = p.value   
        print np.mean(p.value)'''
       
class Battery(Device):
    def __init__(self, name, connections, params=None):
        Device.__init__(self, name, 'B', connections, params)
    def compute_cost(self):
        return np.mean(self.p) 
        
class TransmissionLine(Device):
    def __init__(self, name, connections, params ={'R':1, 'V':1, 'Cmax':1}):
        Device.__init__(self, name, 'T', connections)
    def fx(self,p):
        return 0
    '''def constrains(p):
        con = list()
        con.append(cvx.norm(p,1)/2 <= self.params['Cmax'])
        con.append(p1)'''
        
class Load(Device):
    def __init__(self, name, connections, params = {'l':1}):
        Device.__init__(self, name, 'L', connections)
    def fx(self, p):
        return 0
    def constrains(self, p):
        return [p==self.params['l']]

class DefferableLoad(Device):
    def __init__(self, name, connections, params = {'E':8,'Lmax':1}):
        Device.__init__(self, name, 'DL', connections, params)
    def fx(self,p):
        return 0
    def constrains(self, p):
        con = list()
        con.append(cvx.sum_entries(p)>=self.params['E'])
        con.append(p>=0)
        con.append(p<=self.param['Lmax'])

class CurtalibleLoad(Device):
    def __init__(self, name, connections):
        Device.__init__(self, name, 'CL', connections)
    def compute_cost(self):
        return np.mean(self.p) 
