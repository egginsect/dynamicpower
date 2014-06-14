from terminal_th import *
class PowerSystem(object):
       self.phase = 0
       self.devicelist = list()
       self.netlist = list()     
       self.adjmat = adjmat
       self.terminal_count = {'N':0, 'G':0, 'B':0, 'T':0, 'DL':0, 'CL':0}
       self.adddterminals(terminals)
       self.device_table={}
       self.net_table={}

