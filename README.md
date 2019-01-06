# Bootstrap confidence intervals
This module implements the non-parametric bootstrap confidence intervals
described in 'Bootstrap Confidence Intervals' by T. DiCiccio and B. Efron.

## Installation
Package is available on PyPI and can be installed using pip:  
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
