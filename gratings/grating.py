import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

from math import exp, isclose
from random import gauss, randint

class Grating:
    def __init__(self, params, wavelengths, target = None):
        self.params, self.wls = list(params), wavelengths
        self.labels, self.fom, self.trans, self.peak = 4 * (None,)
        self.target = target if target else (self.wls[0] + self.wls[1])/2

    def __str__(self):
        strrep = ', '.join(["{} = {:.4g}".format(*i) for i in zip(self.labels, self.params)])
        if self.peak:
            strrep += ", peak at {:.3f}; {:.1%} tall and {:.3g} wide".format(*self.peak, self.linewidth)
        if self.fom:
            strrep += ', fom: {:.3f}'.format(self.fom)
        return strrep

    def __eq__(self, rhs):
        if self.__class__ != rhs.__class__ or self.wls != rhs.wls:
            return False
        if any([not isclose(l, r) for (l, r) in zip(self.params, rhs.params)]):
            return False
        return True

    def findpeak(self):
        self.peak = max(self.trans, key = lambda x: x[1])
        peakidx = self.trans.index(self.peak)
        if peakidx == 0 or peakidx == len(self.trans) - 1:
            self.peak = None
        else:
            interp_wl = lambda tr, i, goal: tr[i][0] + (goal - tr[i][1]) \
                    * (tr[i + 1][0] - tr[i][0]) / (tr[i + 1][1] - tr[i][1])

            leftpt = next((pt for pt in self.trans[peakidx - 1::-1] if pt[1] < self.peak[1]/2), None)
            rightpt = next((pt for pt in self.trans[peakidx + 1:] if pt[1] < self.peak[1]/2), None)
            
            if leftpt and rightpt:
                leftwl = interp_wl(self.trans, self.trans.index(leftpt), self.peak[1]/2)
                rightwl = interp_wl(self.trans, self.trans.index(rightpt) - 1, self.peak[1]/2)
                self.linewidth = rightwl - leftwl
            else:
                self.peak = None


    def _calcfom(self):
        if self.fom is None:
            self.findpeak()
            self.fom = (sum([t**2 for (wl, t) in self.trans])/len(self.trans))**(-1/2)
            if self.peak:
                try:
                    self.fom *= self.peak[1]**2 * (self.wls[1] - self.wls[0]) / self.linewidth\
                            * exp(-(10*(self.target - self.peak[0]) / (self.wls[1] - self.wls[0]))**2)
                except TypeError:
                    print("TypeError; self.peak =", self.peak)
                    raise SystemExit

    def mutate(self):
        childparams = [round(gauss(1, 0.1)*p, 4) for p in self.params]
        child = self.__class__(childparams, self.wls, self.target)
        return child

    def crossbreed(self, rhs):
        childparams = [p[randint(0, 1)] for p in zip(self.params, rhs.params)]
        child = self.__class__(childparams, self.wls, self.target)
        return child
