# Bootstrap confidence intervals
This module implements the non-parametric bootstrap confidence intervals
described in 'Bootstrap Confidence Intervals' by T. DiCiccio and B. Efron.

## Installation
Package is [available on PyPI](https://pypi.org/project/bootstrap-interval/) and can be installed using pip:  
``` pip install bootstrap-interval ```
## Files description
* bootstrap_interval.py contains the package source code
* code.py is an example of package usage
## Usage
The Boostrap class contains the resampling distribution for a given statistics

class bootstrap_interval.**Bootstrap**(sample, stat='mean', n_iter=10000, sample_size=None)

Parameters:  
  **sample**: data sample  
  **stat**: statistics to estimate. Can be either 'mean', 'std' or any function callable on sample  
  **n_iter**: number of resamples to use  
  **sample_size**: size of resamples. If None, equals to the size of sample  
Attributes:  
  **computed**: flag if the resampling distribution was already computed  
  **distribution**: distribution of the statistics on bootstrap resamples
  
Methods:
    **get_distribution**(): returns the resampling distribution  
    **get_confidence_interval**(alpha, method='percentile'): returns the pair (left, right), left and right endpoints of confidence interval

get_confidence_interval(alpha, method)
Arguments:  
  **alpha**: significance level, so that 1-alpha is the confidence level  
  **method**: one of 'percentile', 'sampling', 'bias_corrected': method to construct the confidence interval  
  if **method**="sampling" then confidence interval of the bootstrap distribution is used  
  if **method**="percentile"  then the percentile method is used (Ch. 23.1 of van der Vaart)  
  if **method**="bias_corrected" then the bias corrected method with acceleration is used (formula 2.3 of DiCiccio and Efron)
  
 ## Example
code.py contains the following simulation:
A 1000 samples of length 100 are drawn from uniform distribution U(0,1).
For each of the samples compute a 95%-confidence interval for the standard deviation using each of 3 methods:
```
for i in range(1000):
    sample = np.random.uniform(size=10**2)
    bs = bootstrap_interval.Bootstrap(sample, stat='std')
    left_bc, right_bc = bs.get_confidence_interval(0.05, method='bias_corrected')
    left_perc, right_perc = bs.get_confidence_interval(0.05, method='percentile')
    left_sampling, right_sampling = bs.get_confidence_interval(0.05, method='sampling')
```                                    
Then we compute how many intervals contain the true staandard deviation value: sqrt(1/12)  
bias_corrected method: 944  
percentile method: 940  
sampling method: 938  
sizes of the confidence intervals:
![alt text](https://raw.githubusercontent.com/neshitov/bootstrap/master/Figure_1.png)
So the three methods show pretty close results

## References:
* A. van der Vaart. Asymptotic statistics, 1998
* T. DiCiccio, B. Efron. Bootstrap Confidence Intervals. Statistical Science 1996, Vol. 11, No. 3, 189–228

