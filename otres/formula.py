ves = 50
povtor = 8

def brzycki(w,r):
    return(w*(36/(37-r)))
def lombardi(w,r):
    return(w*(r**0.10))
def oconner(w,r):
    return(w*(1+(r/40)))