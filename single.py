from lib.generation import Generation
from gratings.zcg import ZCG

import matplotlib.pyplot as plt

def main():
    #dimensions
    d = 4.681
    ff = 0.6371
    tline = 2.8206
    tslab = 1.6668
    tstep = 0.0865

    g = ZCG((d, ff, tline, tslab, tstep), (8, 12, 2001), target = 9.7)
    g.evaluate()
    print(g)
    print("RMS transmittance:",(sum([t**2 for (wl, t) in g.trans])/len(g.trans))**(1/2))
    plt.plot(*zip(*g.trans))
    plt.show()

if __name__ == "__main__":
    main()
