import numpy as np

class network:

    def __init__(self, N, delta=0.01, start=[], lambda_junction=0.01, f=None):

        if start==[]:
            self.x = np.random.uniform(0,1,N)

        else:
            self.x = np.array(start)

        if f==None:
            self.f = self.expo

        else:
            self.f = f

        self.delta = delta
        self.N = N
        self.lambda_junction = lambda_junction

    def expo(self, x):  # note parameters
        return np.exp(2 * x) - 0.999999 #firing rate is not 0 to avoid division by 0 in step

    def step(self):

        tau1 = np.random.exponential(1/self.f(self.x))

        spiked = tau1 <=self.delta

        K = spiked.sum()

        spike_increments = ((spiked*-1)+K)/self.N

        avg = self.x.mean()

        junction_increments = self.lambda_junction*(avg-self.x)

        self.x += junction_increments

        j = np.where(spiked)

        self.x[j] = 0
        self.x+=spike_increments

        return spiked, self.x




