def deltaPhi(a,b):
    dphi = fabs(a.phi() - b.phi())
    if (dphi <= pi): return dphi
    else: return 2*pi - dphi
        

def deltaR(a,b):
    dphi = deltaPhi(a,b)
    return hypot((a.eta()-b.eta()),dphi)

