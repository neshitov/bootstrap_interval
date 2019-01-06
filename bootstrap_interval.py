'''
Module for statistical bootstrapping.
Requirements: numpy 1.15.4
              scipy 1.1.0
'''
import numpy as np
from scipy.stats import norm

class Bootstrap:
    '''
    The Boostrap class contains the resampling distribution for a given statistics
    instance parameters:
    sample: the data sample, one-dimensional numpy array
    stat: the statistics to estimate. Must be either one of ['mean','std'] or a
          callable function that returns the statistic applied to a sample, e.g.
          median, quantile, etc.
    n_iter: number of iterations for resampling distribution. By default 10000
    sample_size: size of resampling sample. If None, equals to the size of the
                 data sample of the whole data sample
    distribution: resampling distribution of the given statistics, array of
                  shape (n_iter,) consisting of values of statistics on the
                  bootstrap samples
    computed: a flag that shows if bootstrap distribution is stored in memory
    '''
    def __init__(self, sample, stat='mean', n_iter=10000, sample_size=None):
        ''' creates the class instance. does not compute the distribution'''
        self.sample = sample
        self.stat = stat
        self.n_iter = n_iter
        self.sample_size = sample_size
        self.computed = False
        self.distribution = None
        if not callable(self.stat):
            assert self.stat in ['mean', 'std'], 'stat must be callable or one \
                                                  of "mean", "std" '
            self.stat = {'mean': np.mean, 'std': np.std}[self.stat]
        if self.sample_size is None:
            self.sample_size = sample.shape[0]

    def get_distribution(self):
        ''' returns the resampling distribution'''
        if not self.computed:
            self.distribution = np.zeros(self.n_iter)
            bootstrap_samples = np.random.choice(self.sample,
                                                 size=(self.n_iter,
                                                       self.sample_size))
            self.distribution = np.apply_along_axis(self.stat, 1, bootstrap_samples)
            self.computed = True
        return self.distribution

    def get_confidence_interval(self, alpha, method='percentile'):
        ''' method computes the non-parametric confidence interval of the statistics
        with significance level alpha
        Args:
            alpha: significance level
            method: one of ['percentile','sample','bias_corrected']
                    if method='sample' the interval is constructed from bootstrap
                    distribution quantiles
                    if method='percentile' the intrval is constructed using
                    percentile method (Ch. 23.1 van der Vaart, 'Asymptotic
                    statistics')
                    if method='bias_corrected' the interval is constructed using
                    the accelerated bias correction method (formula (2.3) of
                    T.DiCiccio, B.Efron, 'Bootstrap confidence intervals')
        Returns:
            [left,right]: endpoints of confidence interval
        '''
        self.distribution = self.get_distribution()
        assert method in ['percentile', 'sampling', 'bias_corrected'], 'method \
                should be one of ["percentile", "sampling", "bias_corrected"]'
        if method == 'percentile':
            theta = self.stat(self.sample)
            xi_left, xi_right = np.quantile((self.distribution - theta),
                                            [alpha/2, 1-alpha/2])
            return np.array([theta - xi_right, theta - xi_left])

        elif method == 'bias_corrected':
            theta_hat = self.stat(self.sample)
            fraction = np.sum(self.distribution < theta_hat) / len(self.distribution)
            z_0 = norm.ppf(fraction)
            n = len(self.sample)
            U = np.zeros(n)
            for i in range(n):
                U[i] = (n-1)*(theta_hat - self.stat(np.delete(self.sample, i)))
            # formula (6.6)  of DiCiccio, Efron
            a_hat = 1/6 * np.sum(np.power(U, 3)) / (np.sum(np.power(U, 2))**(1.5))
            def BC(level, z0, a):
                ''' right-hand side of formula (2.3)'''
                z_alpha = norm.ppf(level)
                return norm.cdf(z0 + (z0 + z_alpha) / (1 - a*(z0 + z_alpha)))
            return np.quantile(self.distribution, [BC(alpha/2, z_0, a_hat),
                                                   BC(1 - alpha/2, z_0, a_hat)])
        return np.quantile(self.distribution, [alpha/2, 1-alpha/2])
