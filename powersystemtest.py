from powersystem import *
import pdb
b = np.array([[1,0],[0,1]])
a = ['G','G']
ps = PowerSystem(a,b)
ps.start_simulations(10)
pdb.set_trace()
