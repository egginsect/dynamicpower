from terminal import *
from multiprocessing import Pool
class PowerSystem(object):
    def __init__(self, terminals, adjmat):
       self.devicelist = list()
       self.netlist = list()     
       self.adjmat = adjmat
       self.terminal_count = {'N':0, 'G':0, 'B':0, 'T':0, 'DL':0, 'CL':0}
       self.adddterminals(terminals)

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
            
   
        
         
