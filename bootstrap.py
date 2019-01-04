import numpy as np
import statsmodels.api as sm

class Bootstrap:
    def __init__(self, sample, stat = 'mean', n_iter = 10000, sample_size = None,
                 random_seed = None):
        self.sample = sample
        self.stat = stat
        self.n_iter = n_iter
        self.sample_size = sample_size
        self.computed = False
        self.distribution = None
        self.seed = random_seed
        if not callable(self.stat):
            self.stat = {'mean': np.mean, 'std': np.std}[self.stat]
        if self.sample_size is None:
            self.sample_size = sample.shape[0]

    def get_distribution(self):
        np.random.seed(self.seed)
        if not self.computed:
            self.distribution = np.zeros(self.n_iter)
            bootstrap_samples = np.random.choice(self.sample,
                                                 size=(self.n_iter,
                                                       self.sample_size))
            self.distribution = np.apply_along_axis(self.stat, 1, bootstrap_samples)
            self.computed = True
        return self.distribution

    def get_confidence_interval(self, alpha):
        self.distribution = self.get_distribution()
        return np.percentile(self.distribution,[(100-alpha)/2,100-(100-alpha)/2])
