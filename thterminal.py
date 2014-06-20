import numpy as np
from threading import Thread
import threading
import Queue
from proximal import *
class Terminal(Thread):
    def __init__(self, name, terminal_type, connections, terminals, params = None):
        Thread.__init__(self)
        self.connections = [idx for idx, val in enumerate(connections) if val is 1]
        self.name = name
        self.terminal_type = terminal_type
        self.T = 10 
        self.pbar = 1
        self.u = np.random.uniform(size=(10,1))
        self.params = params
        self.state = 'idle'  
        self.terminals = terminals

 
class Net(Terminal):
    def __init__(self, name, connections, terminals, params = None):
        Terminal.__init__(self, name, 'Net', connections, terminals, params)
        self.power_imbalance = None
        self.device_powers = Queue.Queue(len(self.connections))
            
    def compute_power_imbalance(self): 
        self.power_imbalance = np.zeros((self.T, 1))
        for i in range(len(self.connections)):
            self.power_imbalance = self.power_imbalance + self.device_powers.get()/len(self.connections) 

    def update_price(self):
        self.u = self.u + self.power_imbalance
    def put_power_profile(self, p):
        try:
            self.device_powers.put(p)
        except:
            print self.name+'\'s queue is full'

    def run(self):
        print 'updating', self.name 
        self.compute_power_imbalance()
        self.update_price()

class Device(Terminal):
    def __init__(self, name, device_type, connections, terminals, params):
        Terminal.__init__(self, name, 'Device', connections, terminals, params)
        self.device_type = device_type
        self.p = 0 
        self.price = Queue.Queue(1) 
        self.power_imbalance = Queue.Queue(1)
        self.rho=1
        self.price.put(np.zeros((self.T,1)))
        self.power_imbalance.put(0)

    def cost_function(self, p):
        return prox_operator(self.fx, p, self.rho, self.power_imbalance.get(1,True)+self.price.get(1,True))

    def solve_problem(self):
        p = cvx.Variable(self.T)
        objective = cvx.Minimize(self.cost_function(p))
        constraints = self.constrains(p)
        prob = cvx.Problem(objective, constraints)
        prob.solve()
        self.p = p.value   

    def send_power_profile(self): 
        for i in self.connections:
            print self.p
            self.terminals[i].put_power_profile(self.p)
    def run(self): 
        print self.name, 'is running'
        self.solve_problem()
        self.send_power_profile()

class Generator(Device):
    def __init__(self, name, connections, terminals, params={'alpha':1,'beta':1, 'Cmax':1}):
        Device.__init__(self, name, 'G', connections, terminals, params)

    def fx(self,p):
        return self.params['alpha']*cvx.sum_squares(p)+self.params['beta']*cvx.sum_entries(p)


    def constrains(self,p):
        con = list()
        for i in range(1, p.size[0]):
            con.append(p[i,:]-p[i-1,:]<=self.params['Cmax'])
        return con
    


class Battery(Device):
    def __init__(self, name, connections, terminals, params=None):
        Device.__init__(self, name, 'B', connections, terminals, params)
        self.states = ('recharge', 'discharge')
    def fx(self,p):
        return 0
    def constrains(self,p):
        return []

class Load(Device):
    def __init__(self, name, connections, terminals, params={'l':1}):
        Device.__init__(self, name, 'L', connections, terminals, params)
    def fx(self,p):
        return 0
    def constrains(self,p):
        return [p==self.params['l']]

class DefferableLoad(Device):
    def __init__(self, name, connections, terminals, params={'E':8, 'Lmax':1}):
        Device.__init__(self, name, 'DL', connections, terminals, params)
    def fx(self,p):
        return 0
    def constrains(self, p):
        con = list()
        con.append(cvx.sum_entries(p)>=self.params['E'])
        con.append(p>=0)
        con.append(p<=self.params['Lmax'])
        return con

class CurtailibleLoad(Device):
    def __init__(self, name, connections, terminals, params={'alpha':1}):
        Device.__init__(self, name, 'CL', connections, terminals, params)
        self.params['l']= np.ones((self.T,1))
    def fx(self,p):
        return cvx.sum_entries(cvx.pos(self.params['l']-p))
    def constrains(self, p):
        return []
