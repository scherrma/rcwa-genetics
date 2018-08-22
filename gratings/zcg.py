import S4
from gratings.grating import Grating

import numpy as np
import scipy.interpolate as interp
from scipy.constants import nu2lambda
import lib.helpers as h

class ZCG(Grating):
    si_n = interp.interp1d(*zip(*[[nu2lambda(float(f))*10**6, n] for (f, n) in h.opencsv('materials/silicon_n.csv',1)]))
    si_k = interp.interp1d(*zip(*[[nu2lambda(float(f))*10**6,n] for (f, n) in h.opencsv('materials/silicon_k.csv',1)]))

    def __init__(self, params, wavelengths, target):
        super().__init__(self, params, wavelengths, target)
        self.d, self.ff, self.tline, self.tslab, self.tstep = params
        self.labels = ['d','ff','tline','tslab','tstep']
        if self.tstep > self.tline:
            raise ValueError("tstep cannot be larger than tline")
    
    def evaluate(self):
        if self.fom is None:
            S = S4.New(self.d, 20)
        
            #materials
            S.AddMaterial("Vacuum", 1)
            S.AddMaterial("Silicon", 1) #edited later per wavelength

            #layers
            S.AddLayer('top', 0, "Vacuum")
            S.AddLayer('step', self.tstep, "Vacuum")
            S.AddLayer('lines', self.tline - self.tstep, "Vacuum")
            S.AddLayer('slab', self.tslab, "Silicon")
            S.AddLayer('bottom', 0, "Vacuum")

            #patterning
            S.SetRegionRectangle('step', 'Silicon', (-self.d*self.ff/4, 0), 0, (self.d*self.ff/4, 0))
            S.SetRegionRectangle('lines', 'Silicon', (0,0), 0, (self.d*self.ff/2, 0))

            #light
            S.SetExcitationPlanewave((0,0),0,1)

            self.trans = []
            for wl in np.linspace(*self.wls):
                S.SetFrequency(1/wl)
                S.SetMaterial('Silicon', complex(self.__class__.si_n(wl), self.__class__.si_k(wl))**2)
                self.trans.append((wl, float(np.real(S.GetPowerFlux('bottom')[0]))))
            self._calcfom()
        
        return self.fom
