from thpowersystem import *
import pdb
b = [[0,0,1],[0,0,1],[1,1,0]]
a = ['G','G','N']
ps = PowerSystem(a,b)
ps.device_update()
#print ps.terminals[2].device_powers.get()

ps.net_update()
print ps.terminals[2].power_imbalance
pdb.set_trace()
