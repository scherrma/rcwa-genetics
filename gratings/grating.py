import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

import S4
import numpy as np
from math import exp, isclose
from random import gauss, randint

class Grating:
    def __init__(self, params, wavelengths, target = None, resample = False):
        self.params, self.resample = tuple(params), resample
        self.wls = (wavelengths[0], wavelengths[1], wavelengths[2] // (1 + int(resample)))
        self.labels, self.fom, self.trans, self.peak = 4 * (None,)
        self.target = target if target else (self.wls[0] + self.wls[1])/2

    def __str__(self):
        strrep = ', '.join(["{} = {:.4g}".format(*i) for i in zip(self.labels, self.params)])
        if self.peak:
            strrep += ", peak at {:.3f}; {:.1%} tall and {:.3g} wide".format(*self.peak, self.linewidth)
        if self.fom:
            strrep += ', fom: {:.3f} (target {:.4g})'.format(self.fom, self.target)
        return strrep

    def __eq__(self, rhs):
        return self.__class__ == rhs.__class__ and self.wls == rhs.wls\
                and all([isclose(l, r) for (l, r) in zip(self.params, rhs.params)])

    def mutate(self):
        childparams = [round(gauss(1, 0.1)*p, 4) for p in self.params]
        return self.__class__(childparams, self.wls, self.target)

    def crossbreed(self, rhs):
        childparams = [p[randint(0, 1)] for p in zip(self.params, rhs.params)]
        return self.__class__(childparams, self.wls, self.target)

    def setparam(self, param, value, mode = "="):
        lbl_idx = self.labels.index(param)
        assert lbl_idx is not None, param + " is not a parameter of " + self.__name
        assert mode in ['=', '<', '>'], mod + " is not a supported mode of setparam"
        if mode == ">":
            self.params[lbl_idx] = max(self.params[lbl_idx], value)
        elif mode == "<":
            self.params[lbl_idx] = min(self.params[lbl_idx], value)
        else:
            self.params[lbl_idx] = value
        self.__init__(self.params, self.wls, self.target)

    def evalAt(self, wl):
        self.sim.SetFrequency(1/wl)
        self.setmaterials(wl)
        return float(np.real(self.sim.GetPowerFlux('bottom')[0]))

    def evaluate(self):
        if self.fom is None:
            self.trans = [(wl, self.evalAt(wl)) for wl in np.linspace(*self.wls)]
            self._findpeak()
            if self.resample and self.peak is not None:
                focuswl = (max(self.wls[0], self.peak[0] - 2*self.linewidth),\
                        min(self.wls[1], self.peak[0] + 2*self.linewidth), self.wls[2])
                self.trans += [(wl, self.evalAt(wl)) for wl in np.linspace(*focuswl)]
                self.trans = sorted(list(set(self.trans))) #delete duplicates
                self.peak = None
                self._findpeak()
            self._calcfom()
        return self.fom
    
    def _findpeak(self):
        self.peak = max(self.trans, key = lambda x: x[1])
        peakidx = self.trans.index(self.peak)
        if peakidx == 0 or peakidx == len(self.trans) - 1:
            self.peak = None
        else:
            interp_wl = lambda tr, i, goal: tr[i][0] + (goal - tr[i][1])\
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
        self.fom = 0
        for i in range(len(self.trans) - 1):
            self.fom += (self.trans[i + 1][0] - self.trans[i][0]) * (self.trans[i+1][1] + self.trans[i][1])**2 / 4
        self.fom = (self.fom / (self.wls[1] - self.wls[0]))**(-1/2)

        self._findpeak()
        if self.fom > 20 and self.peak:
            self.fom *= max(1, self.peak[1]**2 * self.target / self.linewidth\
                    * exp(-25*(1 - self.peak[0] / self.target)**2))
