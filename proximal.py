import cvxpy as cvx
def prox_l1(v, lbd):
    x = cvx.max_entries(0, v-lbd) - cvx.max_entries(0, -v - lbd)
    return x

def prox_quad(v, lbd, A, b)
    rho = 1/lbd
    n = A.shape
