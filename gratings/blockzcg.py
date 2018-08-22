import S4
from gratings.grating import Grating

import numpy as np
import scipy.interpolate as interp
from scipy.constants import speed_of_light
import lib.helpers as h

class BlockZCG(Grating): #2D block ZCG
    si_n = interp.interp1d(*zip(*[[((speed_of_light*10**6)/float(f)),n] for f,n in h.opencsv('materials/silicon_n.csv',1)]))
    si_k = interp.interp1d(*zip(*[[((speed_of_light*10**6)/float(f)),n] for f,n in h.opencsv('materials/silicon_k.csv',1)]))

    def __init__(self, params, wavelengths, target):
        Grating.__init__(self, params, wavelengths, target)
        self.d, self.ff, self.tblocks, self.tslab = params
        self.labels = ['d','ff','tblocks', 'tslab']
    
    def evaluate(self, fbasis = 30):
        if self.fom is None:
            S = S4.New(Lattice=((self.d,0), (0, self.d)), NumBasis=fbasis)
        
            #materials
            S.AddMaterial("Vacuum",1)
            S.AddMaterial("Silicon",1) #edited later by wavelength

            #layers
            S.AddLayer('top',0,"Vacuum")
            S.AddLayer('blocks',self.tblocks,"Vacuum")
            S.AddLayer('slab',self.tslab,"Silicon")
            S.AddLayer('bottom', 0, "Vacuum")

            #patterning
            S.SetRegionRectangle('blocks','Silicon',(0,0),0,(self.d*self.ff/2,self.d*self.ff/2))

            #light
            S.SetExcitationPlanewave((0,0),0,1)
            self.trans = []
            for wl in np.linspace(*self.wls):
                S.SetFrequency(1/wl)
                S.SetMaterial('Silicon', complex(self.__class__.si_n(wl), self.__class__.si_k(wl))**2)
                self.trans.append((wl, float(np.real(S.GetPowerFlux('bottom')[0]))))
            self._calcfom()
            self.findpeak()
