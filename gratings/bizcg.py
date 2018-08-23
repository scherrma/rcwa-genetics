import S4
from gratings.grating import Grating
from random import random

import numpy as np
import scipy.interpolate as interp
from scipy.constants import nu2lambda
import lib.helpers as h


class BiZCG(Grating):
    si_n = interp.interp1d(*zip(*[[nu2lambda(float(f))*10**6, n] for (f, n) in h.opencsv('materials/silicon_n.csv',1)]))
    si_k = interp.interp1d(*zip(*[[nu2lambda(float(f))*10**6,n] for (f, n) in h.opencsv('materials/silicon_k.csv',1)]))

    def __init__(self, params, wavelengths, target, angle = 5):
        super().__init__(params, wavelengths, target)
        self.labels = ['d','ff','tline1','tline2','tslab', 'angle']
        self.d, self.ff, self.tline1, self.tline2, self.tslab, self.angle = params
        if self.tline2 > self.tline1:
            self.tline2, self.tline1 = self.tline1, self.tline2
        if self.tslab + self.tline2 < 0:
            raise ValueError("-self.tline > self.tslab")
   
    def evaluate(self):
        if self.fom is None:
            S = S4.New(self.d, 20)
        
            #materials
            S.AddMaterial("Vacuum",1)
            S.AddMaterial("Silicon",1) #edited later per wavelength

            #layers
            S.AddLayer('top',0,"Vacuum")
            S.AddLayer('line1',self.tline1 - self.tline2,"Vacuum")
            S.AddLayer('line2',self.tline2 - self.tslab,"Vacuum")
            S.AddLayer('slab',self.tslab,"Silicon")
            S.AddLayer('bottom', 0, "Vacuum")

            #patterning
            S.SetRegionRectangle('line1','Silicon',(-3*self.d*self.ff/8,0),0,(self.d*self.ff/8,0))
            S.SetRegionRectangle('line2','Silicon',(-3*self.d*self.ff/8,0),0,(self.d*self.ff/8,0))
            S.SetRegionRectangle('line2','Silicon',(self.d*self.ff/8,0),0,(self.d*self.ff/8,0))


            all_trans = []
            for theta in (0, self.angle):
                #light
                S.SetExcitationPlanewave((0, 0), np.sin(theta), np.cos(theta))
                
                self.trans = []
                for wl in np.linspace(*self.wls):
                    S.SetFrequency(1/wl)
                    S.SetMaterial('Silicon', complex(self.__class__.si_n(wl), self.__class__.si_k(wl))**2)
                    self.trans.append((wl, float(np.real(S.GetPowerFlux('bottom')[0]))))
                all_trans.append(self.trans)

            trans_metadata = []
            for trans in all_trans:
                self.trans = trans
                self.fom, self.peak, self.linewidth = 3 * (None,)
                self.findpeak()
                self._calcfom()
                trans_metadata.append((self.fom, self.peak, self.linewidth))
            self.trans = all_trans
            self.fom, self.peak, self.linewidth = max(trans_metadata)
        return self.fom

    def mutate(self):
        child = Grating.mutate(self)
        if random() > 2/3:
            child.params[3] = -min(self.tline2, 0.9*self.tslab)
        child.params[5] = self.angle
        return child

    def crossbreed(self, rhs):
        child = Grating.mutate(self)
        child.params[5] = self.angle
        return child
