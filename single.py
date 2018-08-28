from lib.generation import Generation
import matplotlib.pyplot as plt

from gratings.zcg import ZCG
from gratings.hcg import HCG
from gratings.blockzcg import BlockZCG
from gratings.nirzcg import NIRZCG


def main():
   #dimensions
    d = 4.681
    ff = 0.6371
    tline = 2.8206
    tslab = 1.6668
    tstep = 0.0865
    wavelengths = (8, 12, 301)
    target = 9.4
  
    g = ZCG((d, ff, tline, tslab, tstep), wavelengths, target, resample = True)
    g.evaluate()
    print(g)
    plt.plot(*zip(*g.trans))
    plt.show()

if __name__ == "__main__":
    main()
