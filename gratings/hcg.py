import S4
from gratings.grating import Grating

import numpy as np
import scipy.interpolate as interp
from scipy.constants import nu2lambda
from lib.helpers import opencsv

class HCG(Grating):
    si_n = interp.interp1d(*zip(*[[nu2lambda(float(f))*10**6, n] for (f, n) in opencsv('materials/silicon_n.csv',1)]))
    si_k = interp.interp1d(*zip(*[[nu2lambda(float(f))*10**6,n] for (f, n) in opencsv('materials/silicon_k.csv',1)]))

    def __init__(self, params, wavelengths, target = None, resample = False):
        super().__init__(params, wavelengths, target, resample)
        self.labels = ['d','ff','tline','tair','tstep']
        d, ff, tline, tair, tstep = params
        assert tline > tstep, "tstep cannot be larger than tline"

        #create simulation
        self.sim = S4.New(d, 20)
        
        self.sim.AddMaterial("Vacuum", 1)
        self.sim.AddMaterial("Silicon", 0) #edited later in setmaterials

        self.sim.AddLayer('top', 0, "Vacuum")
        self.sim.AddLayer('step', tstep, "Vacuum")
        self.sim.AddLayer('lines', tline - tstep, "Vacuum")
        self.sim.AddLayer('airgap', tair, "Vacuum")
        self.sim.AddLayer('bottom', 0, "Vacuum")

        self.sim.SetRegionRectangle('step', 'Silicon', (-d*ff/4, 0), 0, (d*ff/4, 0))
        self.sim.SetRegionRectangle('lines', 'Silicon', (0,0), 0, (d*ff/2, 0))

        self.sim.SetExcitationPlanewave((0,0),0,1)

    def setmaterials(self, wl):
        self.sim.SetMaterial('Silicon', complex(self.__class__.si_n(wl), self.__class__.si_k(wl))**2)
