import numpy as np
from proximal import *
class Node(object):
    def __init__(self, name, node_type, connections, params):
        self.name = name
        self.node_type = node_type
        self.T = 10 
        self.pbar = 1
        self.u = np.random.uniform(size=(10,1))
        self.params = params
        self.connections = connections

class Net(Node):
    def __init__(self, name, connections, params=None):
        Node.__init__(self, name, 'Net', connections, params)
        self.power_buffer = [np.zeros([self.T,1])]*len(connections)
        self.power_imbalance = None
    def compute_power_imbalance(self):
        self.power_imbalance = sum(self.power_buffer)/len(self.connections)
        return self.power_imbalance
        
    def compute_price(self):
        self.u = self.u + self.compute_power_imbalance()
        print self.name, 'update_price'
    
    def set_power_imbalance(self, p): 
        pd = np.mean(p) 

class Device(Node):
    def __init__(self, name, device_type, connections, params):
        Node.__init__(self, name, 'Device', connections, params)
        self.device_type = device_type
        self.p = cvx.Variable(self.T)
        self.lmbd = 1
       

    def cost_function(self):
        return prox_operator(self.fx, self.p, self.lmbd, self.u+self.pbar)

    def getOriginalObjective(self):
        objective = cvx.Minimize(self.fx())
        constraints = self.constrains()
        prob = cvx.Problem(objective, constraints)
        return prob

class Generator(Device):
    def __init__(self, name, connections, params={'alpha':0.02,'beta':1, 'Pmax':10, 'Pmin':0.01, 'Rmax':10, 'Rmin':0.01}):
        Device.__init__(self, name, 'G', connections, params)
        
    def fx(self):
        return self.params['alpha']*cvx.sum_squares(self.p)+self.params['beta']*cvx.sum_entries(self.p)
    
    def constrains(self):
        con = list()
        con.append(self.p<=-self.params['Pmin'])
        con.append(self.p>=-self.params['Pmax'])
        for i in range(1, self.p.size[0]):
            con.append(self.p[i,:]-self.p[i-1,:]<=self.params['Rmax'])
            con.append(self.p[i,:]-self.p[i-1,:]>=self.params['Rmin'])
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
    def __init__(self, name, connections, params={'Dmax':7,'Cmax':7,'Qmax':35}):
        Device.__init__(self, name, 'B', connections, params)
        self.q_init = 0
    def fx(self):
        return 0
    def constrains(self):
        con = list()
        con.append(self.p>=-self.params['Dmax'])
        con.append(self.p<=self.params['Cmax'])
        for i in xrange(self.p.size[0]-1):
            con.append(self.q_init+cvx.sum_entries(self.p[1:i,:])>=0)
            con.append(self.q_init+cvx.sum_entries(self.p[1:i,:])<=self.params['Qmax'])            
    def compute_cost(self):
        return np.mean(self.p) 
        
class TransmissionLine(Device):
    def __init__(self, name, connections, params ={'R':1, 'V':1, 'Cmax':1}):
        Device.__init__(self, name, 'T', connections, params)
        self.p = [cvx.Variable(self.T), cvx.Variable(self.T)]
    def fx(self):
        return 0
    def constrains(p):
        con = list()
        con.append(cvx.norm(p,1)/2 <= self.params['Cmax'])
        con.append(p[0]+p[1]-self.params['R']/self.params['V']**2*cvx.sum_squares((p[0]-p[1])/2))
        
class FixedLoad(Device):
    def __init__(self, name, connections, params = {'l':1}):
        Device.__init__(self, name, 'FL', connections, params)
    def fx(self):
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

class CurtailableLoad(Device):
    def __init__(self, name, connections):
        Device.__init__(self, name, 'CL', connections)
    def fx(self):
        return 0
    def compute_cost(self):
        return np.mean(self.p) 
