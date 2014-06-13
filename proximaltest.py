from proximal import *
import pdb
import numpy as np
x = cvx.Variable(10)
y = np.random.normal(size=(10,1)) 
def f(x):
    return cvx.sum_entries(x)
cost = prox_operator(f, x, 0.5, y)
pdb.set_trace()
