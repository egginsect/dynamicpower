import cvxpy as cvx
def prox_l1(v, lbd):
    x = max_entries(0, v-lbd) - max(0, -v - lbd)
    return x
