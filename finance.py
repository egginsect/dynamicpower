import numpy as np
import cvxpy as cvx
import pdb
    
n=20
T=15
#risk model
F = np.random.normal(loc=0, scale=1, size=(n,1))
S = F*F.transpose()
d = np.matrix(np.random.normal(loc=0, scale=1, size=(n,1)))
gam = 1

#return model
mu = np.random.normal(loc=0, scale=1, size=(n,1))
#t-cost model
kappa = np.random.uniform(low=0, high=3, size=(n,1))

def f(u):
    return -mu.transpose()*u + (gam/2)*cvx.quad_form(u,S)
def g(u):
    return kappa.transpose()*pow(abs(u), 1.5)
#pdb.set_trace()
#construct problem
xs = cvx.Variable(n)
objective = cvx.Minimize(f(xs))
constraints = [cvx.sum_entries(xs)<=1,xs>=0]
prob = cvx.Problem(objective, constraints)
prob.solve(verbose=True)
