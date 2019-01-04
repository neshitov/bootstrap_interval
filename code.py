import numpy as np
import matplotlib.pyplot as plt
from bootstrap import Bootstrap
import progressbar
from scipy.stats import norm
import time

print(10**(-8))
print(np.version.version)
np.random.seed(42)
N=10
correct=1
check_t=np.zeros(N)
check_perc=np.zeros(N)
check_efron=np.zeros(N)
for i in range(N):
    n_iter=10000
    sample = np.random.randn(10**2)
    bs = Bootstrap(sample, stat = 'std', n_iter = n_iter)
    left_t, right_t = bs.get_confidence_interval(0.05, method = 'bias_corrected')
    left_perc, right_perc = bs.get_confidence_interval(0.05, method = 'percentile')
    left_efron, right_efron = bs.get_confidence_interval(0.05, method = 'efron')
    check_perc[i] = (left_perc<correct) & (right_perc>correct)
    check_t[i] = (left_t<correct) & (right_t>correct)
    check_efron[i] = (left_efron<correct) & (right_efron>correct)
    print('iteration %d, bias_corrected: (%.3f,%.3f)' %(i,left_t,right_t))
    print('iteration %d, percentile: (%.3f,%.3f)' %(i,left_perc,right_perc))
    print('iteration %d, efron: (%.3f,%.3f)' %(i,left_efron,right_efron))
print('afet %d iterations %d bias_corrected correct' %(N,np.sum(check_t)))
print('afet %d iterations %d percentile correct' %(N,np.sum(check_perc)))
print('afet %d iterations %d efron correct' %(N,np.sum(check_efron)))
