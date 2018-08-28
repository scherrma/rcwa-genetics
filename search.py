from datetime import datetime as dt
from lib.generation import Generation
from lib.helpers import writecsv
from termcolor import colored

from gratings.zcg import ZCG
from gratings.hcg import HCG
from gratings.nirzcg import NIRZCG
from gratings.blockzcg import BlockZCG

def main():
    gencount = 5
    gensize = 5

    #dimensions
    d = 4.5
    ff = 2/3
    tline = 2.5
    tslab = 1.5
    tstep = 0.1
    wavelengths = (8, 12, 501)
    target = 10

    thetime = lambda: str(dt.time(dt.now())).split('.')[0]
    g0 = ZCG((d, ff, tline, tslab, tstep), wavelengths, target, resample = True)
    g0.evaluate()
    oldbest = g0
    genbest = list(zip(*g0.trans))
    print(colored("seed:", "cyan"), g0)

    gen = Generation(gensize, g0)
    for i in range(gencount): 
        genheader = thetime() + colored( " gen " + str(i+1), "cyan")
        gen.evaluate(progress_txt = genheader)
        genbest += list(zip(*gen.best.trans))
        #genbest.append([t for (wl, t) in gen.best.trans])
        print(genheader, end = ' ')
        if gen.best.fom > oldbest.fom:
            print(colored("new best grating\n", 'green') + str(gen.best), end = ' ')
            oldbest = gen.best
        print('')
        gen = gen.progeny()

    writecsv("iter_best.csv",list(zip(*genbest)), header = ["seed wl, seed trans"] +\
            ["gen " + str(i) + " wl, gen " + str(i) + " trans" for i in range(gencount)])

if __name__ == "__main__":
    main()
