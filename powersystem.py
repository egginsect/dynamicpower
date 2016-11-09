from node import *
import multiprocessing as mp
deviceFunctions = {'N':Net, 'G':Generator, 'B':Battery, 'T':TransmissionLine, 'FL':FixedLoad}
def unwrap_self_solve_problem_d(arg, **kwarg):
    return PowerSystem.solve_problem_d(*arg, **kwarg)

def net_updater(net):
    net.compute_price()
    
class PowerSystem(object):
    def __init__(self, nodes, adjmat):
       self.nodelist = list()   
       self.adjmat = adjmat
       self.node_count = dict(zip(deviceFunctions.keys(),[0]*len(deviceFunctions.keys())))
       for node in nodes:
           self.adddnode(node)

    def adddnode(self, nodeType, param=None):
        if nodeType not in self.node_count.keys():
            print(nodeType)
            print(self.node_count.keys())
            #raise ValueError('Wrong node type')
        else:
                self.nodelist.append(deviceFunctions[nodeType](nodeType+str(self.node_count[nodeType]), [0], param))
                self.node_count[nodeType]+=1
                
    def solve_problem_d(self, device):
        print 'solve problem for device', device.name
        objective = cvx.Minimize(device.cost_function(p))
        constraints = device.constrains(p)
        prob = cvx.Problem(objective, constraints)
        prob.solve()
        #device.p = p.value 
        print np.mean(p.value)
      
    def device_update(self):
        print 'updating device'
        pool = mp.Pool(len(self.devicelist))
        pool.map(unwrap_self_solve_problem_d, zip([self]*len(self.devicelist), self.devicelist))
  
    def net_update(self):    
        print 'updating net'
        pool = mp.Pool(len(self.netlist))
        pool.map(net_updater, self.netlist)
     
    def start_simulations(self, maxiter):
        for i in xrange(maxiter):
            self.device_update()
            self.net_update()
            
