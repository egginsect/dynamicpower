from terminal import *
class PowerSystem(object):
    def __init__(self, terminals, adjmat):
       self.devicelist = list()
       self.netlist = list()     
       self.adjmat = adjmat
       self.terminal_count = {'N':0, 'G':0, 'B':0, 'T':0, 'DL':0, 'CL':0}
       self.adddterminals(terminals)
       self.device_table={}
       self.net_table={}

    def adddterminals(self, terminals):
        for (terminal,neighbors) in zip(terminals, self.adjmat.tolist()):
            if terminal not in self.terminal_count.keys():
                print 'Wrong terminal type' 
            else:
                if terminal is 'N':
                    self.netlist.append(Net('N'+str(self.terminal_count[terminal]), neighbors))
                elif terminal is 'G':
                    self.devicelist.append(Generator('G'+str(self.terminal_count[terminal]), neighbors))
                elif terminal is 'B':
                    self.devicelist.append(Battery('B'+str(self.terminal_count[terminal]), neighbors))
                elif terminal is 'T':
                    self.devicelist.append(TransmissionLine('T'+str(self.terminal_count[terminal]), neighbors))
                elif terminal is 'DL':
                    self.devicelist.append(DefferableLoad('DL'+str(self.terminal_count[terminal]), neighbors))
                elif terminal is 'CL':
                    self.devicelistnetlist.append(CurtalibleLoad('CL'+str(self.terminal_count[terminal]), neighbors))
                self.terminal_count[terminal]+=1

    def solve_problem(self, device):
        print 'solve problem for device', device.name
        p = cvx.Variable(device.T)
        objective = cvx.Minimize(device.cost_function(p))
        constraints = device.constrain(p)
        prob = cvx.Problem(objective, constraints)
        prob.solve()
        #device.p = p.value 
        print np.mean(p.value)
      
    def device_update(self):
        for device in self.devicelist:
            self.solve_problem(device)
     
    def start_simulations(self, maxiter):
        self.device_update()
      

