import numpy as np
import statsmodels.api as sm
from scipy.stats import norm
#requires numpy 1.15
class Bootstrap:
    def __init__(self, sample, stat = 'mean', n_iter = 10000, sample_size = None):
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
        if not self.computed:
            self.distribution = np.zeros(self.n_iter)
            bootstrap_samples = np.random.choice(self.sample,
                                                 size=(self.n_iter,
                                                       self.sample_size))
            self.distribution = np.apply_along_axis(self.stat, 1, bootstrap_samples)
            self.computed = True
        return self.distribution

    def get_confidence_interval(self, alpha, method = 'percentile'):
        self.distribution = self.get_distribution()
        if method == 'percentile':
            theta = self.stat(self.sample)
            xi_left, xi_right = np.quantile((self.distribution - theta),
                                            [alpha/2, 1-alpha/2])
            return [theta - xi_right, theta - xi_left]

        if method == 'efron':
            return np.quantile(self.distribution, [alpha/2, 1-alpha/2])
#formula 2.3 of efron96
        if method == 'bias_corrected':
            theta_hat = self.stat(self.sample)
            fraction = np.sum(self.distribution < theta_hat) / len(self.distribution)
            z_0 = norm.ppf(fraction)
            n = len(self.sample)
            U = np.zeros(n)
            for i in range(n):
                U[i] = (n-1)*(theta_hat - self.stat(np.delete(self.sample, i)))
            a_hat = 1/6 * np.sum(np.power(U, 3)) / (np.sum(np.power(U, 2))**(1.5)) # formula 6.6 of efron
            def BC(level, z0, a):
                z_alpha = norm.ppf(level)
                return norm.cdf(z0 + (z0 + z_alpha) / (1 - a*(z0 + z_alpha)))
            return np.quantile(self.distribution, [BC(alpha/2, z_0, a_hat),
                                                   BC(1 - alpha/2, z_0, a_hat)])
