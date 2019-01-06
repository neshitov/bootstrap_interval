'''
This is an example of bootstrap_interval module usage.
In this example we draw 1000 samples of length 100
from the uniform distribution U(0,1).

For every sample we compute a bootstrap 95%-confidence interval for
standard deviation using 3 possible methods: smapling, percentile
and bias corrected.

Then we compute the number of confidence intervals that contain the true
standard deviation for each of the methods and display the length distribution
of the confidene intervals.
'''

import numpy as np
import matplotlib.pyplot as plt
import bootstrap_interval
from sys import stdout

np.random.seed(42)
N = 1000
# true value of uniform distribution std
correct_stat = np.sqrt(1 / 12)
# Estimate bootsrap confidence intervals for std of uniform distribution
# of confidence level 95%

# count number of correctly predicted confidence intervals for each method
check_bc = 0
check_perc = 0
check_sampling = 0

# arrays to store lengths of confidence intervals
length_bc = np.zeros(N)
length_perc = np.zeros(N)
length_sampling = np.zeros(N)

for i in range(N):
    stdout.write("\r%d samples processed" % i)
    stdout.flush()

    sample = np.random.uniform(size=10**2)
    bs = bootstrap_interval.Bootstrap(sample, stat='std')

    left_bc, right_bc = bs.get_confidence_interval(
                        0.05, method='bias_corrected')
    left_perc, right_perc = bs.get_confidence_interval(
                            0.05, method='percentile')
    left_sampling, right_sampling = bs.get_confidence_interval(
                                    0.05, method='sampling')

    length_bc[i] = right_bc - left_bc
    length_perc[i] = right_perc - left_perc
    length_sampling[i] = right_sampling - left_sampling

    check_bc += (left_bc < correct_stat) & (right_bc > correct_stat)
    check_perc += (left_perc < correct_stat) & (right_perc > correct_stat)
    check_sampling += (left_sampling <
                       correct_stat) & (right_sampling > correct_stat)

stdout.write("\r   ")
stdout.flush()

print('Among %d samples:' % N)
print('%d correct intervals constructed using bias_corrected method' % check_bc)
print('%d correct intervals constructed using percentile method' % check_perc)
print('%d correct intervals constructed using sampling method' % check_sampling)

# compare the lengths of confidence intervals
plt.subplot(1, 3, 1).set_title('bias corrected')
plt.hist(length_bc)
plt.subplot(1, 3, 2).set_title('percentile method')
plt.hist(length_perc)
plt.subplot(1, 3, 3).set_title('sampling method')
plt.hist(length_sampling)
plt.tight_layout
plt.show()
