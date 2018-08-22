from datetime import datetime as dt
from gratings.zcg import ZCG
from lib.generation import Generation
from lib.helpers import writecsv

from termcolor import colored

def main():
    gencount = 100

    #dimensions
    d = 5
    ff = 2/3
    tline = 2.5
    tslab = 1.5
    tstep = 0.2

    thetime = lambda: str(dt.time(dt.now())).split('.')[0]
    g0 = ZCG((d, ff, tline, tslab, tstep), (8, 12, 2001), target = 10.5)
    g0.evaluate()
    oldbest = g0
    genbest = list(zip(*g0.trans))
    print(colored("seed:", "cyan"), g0)

    gen = Generation(25, g0)
    for i in range(gencount): 
        genheader = thetime() + colored( " gen " + str(i), "cyan")
        gen.evaluate(progress_txt = genheader)
        gen = gen.progeny()
        print(genheader)
        genbest.append([t for wl,t in gen.best.trans])
        if gen.best.fom > oldbest.fom:
            print(colored("new best grating\n", 'green') + str(gen.best))
            oldbest = gen.best

    writecsv("iter_best.csv",list(zip(*genbest)),tuple(["wl",0]+list(range(1,gencount+1))))

if __name__ == "__main__":
    main()
