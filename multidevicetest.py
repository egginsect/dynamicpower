from terminal import *
import multiprocessing
n = 10
A = 1 - np.eye(n)
B = 10*['G'] 
devices = list()
for (idx, item), neighbor in zip(enumerate(B), A.tolist()):
   devices.append(Generator(item+str(idx), neighbor))

def solveproblem(device):
    print 'solve problem for device', device.name
    p = cvx.Variable(device.T)
    objective = cvx.Minimize(device.cost_function(p))
    constraints = device.constrain(p)
    prob = cvx.Problem(objective, constraints)
    prob.solve()
    print p.value

p = multiprocessing.Pool(n)
p.map(solveproblem, devices)
