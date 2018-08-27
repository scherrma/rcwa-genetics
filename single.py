from lib.generation import Generation
from gratings.zcg import ZCG

import matplotlib.pyplot as plt

def main():
    #dimensions
  #  d = 4.681
  #  ff = 0.6371
  #  tline = 2.8206
  #  tslab = 1.6668
  #  tstep = 0.0865
  #  wavelengths = (8, 12, 51)
    d = 4.838
    ff = 0.6528
    tline = 2.682
    tslab = 1.258
    tstep = 0.2187
    wavelengths = (8, 12, 201)
    target = 10.5

    g = ZCG((d, ff, tline, tslab, tstep), wavelengths, target)
    g.adaptiveeval()
    print(g)
    print("RMS transmittance:",(sum([t**2 for (wl, t) in g.trans])/len(g.trans))**(1/2))
    plt.plot(*zip(*g.trans))
    plt.show()

if __name__ == "__main__":
    main()
