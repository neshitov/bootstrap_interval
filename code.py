import numpy as np
import matplotlib.pyplot as plt
from bootstrap import Bootstrap
import progressbar
import time

N=1000

check=np.zeros(N)
for i in range(N):
    n_iter=10000
    sample = np.random.randn(10**2)
    bs = Bootstrap(sample, stat = 'std', n_iter = n_iter)
    left, right = bs.get_confidence_interval(95)
    check[i] = (left < 1) & (right >1)
    print('iteration: #%d, interval:(%.5f,%.5f)' %(i,left,right))
print('after %d iterations got %d correct intervals' %(N,np.sum(check)))
#plt.show()
