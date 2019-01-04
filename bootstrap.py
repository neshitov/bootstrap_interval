import numpy as np
import statsmodels.api as sm

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

    def get_confidence_interval(self, alpha, method = 't_percentile'):
        self.distribution = self.get_distribution()
        if method == 't_percentile':
            theta = self.stat(self.sample)
            sigma = np.std(self.distribution)
            xi_left, xi_right = np.quantile((self.distribution - theta)/(sigma + 10**(-8)),
                                            [alpha/2, 1-alpha/2])
            return [theta - xi_right * sigma, theta - xi_left * sigma]
        if method == 'efron':
            return np.quantile(self.distribution, [alpha/2, 1-alpha/2])
