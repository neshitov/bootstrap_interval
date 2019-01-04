import numpy as np
import matplotlib.pyplot as plt
from bootstrap import Bootstrap
import time

N=1000

check=np.zeros(N)
for i in range(N):
    n_iter=10000
    sample = np.random.randn(10**2)
    bs = Bootstrap(sample,n_iter=n_iter)
    left, right = bs.get_confidence_interval(95)
    check[i] = (left < 0) & (right >0)

print('after %d iterations got %d correct intervals' %(N,np.sum(check)))
#plt.show()
