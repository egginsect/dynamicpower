from thterminal import *
terminals = list()
g = Generator('G', [1], terminals) 
terminals.append(g)
n = Net('N', [0], terminals)
terminals.append(n)
g.start()
g.join()
print n.device_powers.empty()
