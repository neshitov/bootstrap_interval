import numpy as np
import matplotlib.pyplot as plt
from bootstrap import Bootstrap

np.random.seed(42)
N=1000
# true value of uniform distribution std
correct=np.sqrt(1/12)
# Estimate bootsrap confidence intervals for std of uniform distribution
# of confidence level 95%

# array to store 1 if true value is inside the confidence interval
check_bc=np.zeros(N)
check_perc=np.zeros(N)
check_sampling=np.zeros(N)

# length of confidence intervals
length_bc=np.zeros(N)
length_perc=np.zeros(N)
length_sampling=np.zeros(N)

for i in range(N):
    sample = np.random.uniform(size=10**2)
    bs = Bootstrap(sample, stat = 'std')

    left_bc, right_bc = bs.get_confidence_interval(0.05, method = 'bias_corrected')
    left_perc, right_perc = bs.get_confidence_interval(0.05, method = 'percentile')
    left_sampling, right_sampling = bs.get_confidence_interval(0.05, method = 'sampling')

    length_bc[i] = right_bc - left_bc
    length_perc[i] = right_perc - left_perc
    length_sampling[i] = right_sampling - left_sampling

    check_bc[i] = (left_bc<correct) & (right_bc>correct)
    check_perc[i] = (left_perc<correct) & (right_perc>correct)
    check_sampling[i] = (left_sampling<correct) & (right_sampling>correct)

print('after %d iterations %d bias_corrected correct' %(N,np.sum(check_bc)))
print('after %d iterations %d percentile correct' %(N,np.sum(check_perc)))
print('after %d iterations %d sampling correct' %(N,np.sum(check_sampling)))

# compare the lengths of confidence intervals
plt.subplot(1,3,1).set_title('bias corrected')
plt.hist(length_bc)
plt.subplot(1,3,2)
plt.hist(length_perc).set_title('percentile method')
plt.subplot(1,3,3)
plt.hist(length_sampling).set_title('sampling method')
plt.tight_layout
plt.show()
