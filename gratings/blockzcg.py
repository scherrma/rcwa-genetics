import S4
from gratings.grating import Grating

import numpy as np
import scipy.interpolate as interp
from scipy.constants import speed_of_light
from lib.helpers import opencsv

class BlockZCG(Grating): #2D block ZCG
    si_n = interp.interp1d(*zip(*[[((speed_of_light*10**6)/float(f)),n] for f,n in opencsv('materials/silicon_n.csv',1)]))
    si_k = interp.interp1d(*zip(*[[((speed_of_light*10**6)/float(f)),n] for f,n in opencsv('materials/silicon_k.csv',1)]))

    def __init__(self, params, wavelengths, target = None, resample = False, fbases = 30):
        super().__init__(params, wavelengths, target)
        d, ff, tblocks, tslab = params
        self.labels = ['d','ff','tblocks', 'tslab']
           
        #create simulation
        self.sim = S4.New(((d, 0), (0, d)), fbases)
        
        self.sim.AddMaterial("Vacuum", 1)
        self.sim.AddMaterial("Silicon", 0) #edited later in setmaterials

        self.sim.AddLayer('top', 0, "Vacuum")
        self.sim.AddLayer('blocks', tblocks, "Vacuum")
        self.sim.AddLayer('slab', tslab, "Silicon")
        self.sim.AddLayer('bottom', 0, "Vacuum")

        self.sim.SetRegionRectangle('blocks','Silicon',(0,0),0,(d*ff/2, d*ff/2))

        self.sim.SetExcitationPlanewave((0, 0), 0, 1)

    def setmaterials(self, wl):
        self.sim.SetMaterial('Silicon', complex(self.__class__.si_n(wl), self.__class__.si_k(wl))**2)
