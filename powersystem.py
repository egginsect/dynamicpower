from terminal import *
class PowerSystem(object):
    def __init__(self, terminals, adjmat):
       self.devicelist = list()
       self.netlist = list()     
       self.adjmat = adjmat
       self.terminal_count = {'N':0, 'G':0, 'B':0, 'T':0, 'DL':0, 'CL':0}
       self.adddterminals(terminals)

    def adddterminals(self, terminals):
        for terminal in terminals:
            if terminal not in self.terminal_count.keys():
                print 'Wrong terminal type' 
            else:
                if terminal is 'N':
                    self.netlist.append(Net('N'+str(sum(self.terminal_count.values())),None))
                elif terminal is 'G':
                    self.devicelist.append(Generator('G'+str(sum(self.terminal_count.values())),None))
                elif terminal is 'B':
                    self.devicelist.append(Battery('B'+str(sum(self.terminal_count.values())),None))
                elif terminal is 'T':
                    self.devicelist.append(TransmissionLine('T'+str(sum(self.terminal_count.values())),None))
                elif terminal is 'DL':
                    self.devicelist.append(DefferableLoad('DL'+str(sum(self.terminal_count.values())),None))
                elif terminal is 'CL':
                    self.devicelistnetlist.append(CurtalibleLoad('CL'+str(sum(self.terminal_count.values())),None))
                self.terminal_count[terminal]+=1
            
   
        
         
