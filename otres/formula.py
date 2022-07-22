def one_rm(weight, rep):

    def brzycki(w,r):
        return(w*(36/(37-r)))
    def lombardi(w,r):
        return(w*(r**0.10))
    def oconner(w,r):
        return(w*(1+(r/40)))

    b = brzycki(weight, rep)
    l = lombardi(weight, rep)
    c = oconner(weight, rep)

    return(max([b, l, c]))