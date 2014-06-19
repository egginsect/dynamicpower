import numpy as np
from thterminal import *
class PowerSystem(object):
    def __init__(self, terminals, adjmat):
        self.terminals = list()
        self.terminal_count = {'N':0, 'G':0, 'B':0, 'T':0, 'DL':0, 'CL':0}
        self.adjmat = adjmat
        print self.adjmat
        self.adddterminals(terminals)

    def adddterminals(self, terminals):
        for terminal, neighbors in zip(terminals, self.adjmat):
            if terminal not in self.terminal_count.keys():
                print 'Wrong terminal type' 
            else:
                if terminal is 'N':
                    print terminal, neighbors
                    self.terminals.append(Net('N'+str(self.terminal_count[terminal]), neighbors, self.terminals))
                else:
                    if terminal is 'G':
                        self.terminals.append(Generator('G'+str(self.terminal_count[terminal]), neighbors, self.terminals))
                self.terminal_count[terminal]+=1
 
    def device_update(self):
      for t in self.terminals:
          if(t.terminal_type is 'Device'):
              t.start()

      for t in self.terminals:
          if(t.terminal_type is 'Device'):
              t.join()
    
    def net_update(self):
      for t in self.terminals:
          if(t.terminal_type is 'Net'):
              t.start()

      for t in self.terminals:
          if(t.terminal_type is 'Net'):
              t.join()
