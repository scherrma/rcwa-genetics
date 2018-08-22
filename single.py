from lib.generation import Generation
from gratings.zcg import ZCG

import matplotlib.pyplot as plt

def main():
    #dimensions
    d = 5
    ff = 2/3
    tline = 2.5
    tslab = 1.5
    tstep = 0.2

    g = ZCG((d, ff, tline, tslab, tstep), (8, 12, 2001), target = 10.4)
    g.evaluate()
    print(g)
    print("total trans:",(sum([t**2 for (wl, t) in g.trans])/len(g.trans))**(1/2))
    plt.plot(*zip(*g.trans))
    plt.show()

if __name__ == "__main__":
    main()
