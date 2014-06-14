from terminal import *
import multiprocessing as mp
def unwrap_self_solve_problem_d(arg, **kwarg):
    return PowerSystem.solve_problem_d(*arg, **kwarg)

def net_updater(net):
    net.compute_price()
    
class PowerSystem(object):
    def __init__(self, terminals, adjmat):
       self.phase = 0
       self.devicelist = list()
       self.netlist = list()     
       self.adjmat = adjmat
       self.terminal_count = {'N':0, 'G':0, 'B':0, 'T':0, 'DL':0, 'CL':0}
       self.adddterminals(terminals)
       self.device_table={}
       self.net_table={}

    def adddterminals(self, terminals):
        for (idx,terminal),neighbors in zip(enumerate(terminals), self.adjmat.tolist()):
            if terminal not in self.terminal_count.keys():
                print 'Wrong terminal type' 
            else:
                if terminal is 'N':
                    self.netlist.append(Net('N'+str(self.terminal_count[terminal]), np.where(neighbors==6)))
                elif terminal is 'G':
                    self.devicelist.append(Generator('G'+str(self.terminal_count[terminal]), np.where(neighbors==6)))
                elif terminal is 'B':
                    self.devicelist.append(Battery('B'+str(self.terminal_count[terminal]), np.where(neighbors==6)))
                elif terminal is 'T':
                    self.devicelist.append(TransmissionLine('T'+str(self.terminal_count[terminal]), np.where(neighbors==6)))
                elif terminal is 'DL':
                    self.devicelist.append(DefferableLoad('DL'+str(self.terminal_count[terminal]), np.where(neighbors==6)))
                elif terminal is 'CL':
                    self.devicelistnetlist.append(CurtalibleLoad('CL'+str(self.terminal_count[terminal]), np.where(neighbors==6)))
                self.terminal_count[terminal]+=1

    def solve_problem_d(self, device):
        print 'solve problem for device', device.name
        p = cvx.Variable(device.T)
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
            
