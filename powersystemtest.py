from powersystem import *
import pdb
b = 1-np.eye(3)
a = ['G','G','N']
ps = PowerSystem(a,b)
ps.start_simulations(10)
pdb.set_trace()
