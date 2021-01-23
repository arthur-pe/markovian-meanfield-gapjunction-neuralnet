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

    def expo(self, x):
        return np.exp(2 * x) - 1

    def step(self):

        tau1 = np.random.exponential(1/(self.f(np.maximum(self.x,0.0001))))#0.0001 is here to avoid division by 0

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


class network_leaky:

    def __init__(self, N, delta=0.01, start=[], lambda_junction=0.01, leak_rate=0.005, f=None):

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
        self.leak_rate = leak_rate

    def expo(self, x):  # note parameters
        return np.exp(2 * x) - 1

    def step(self):

        tau1 = np.random.exponential(1/(self.f(np.maximum(self.x,0.0001))))#0.0001 is here to avoid division by 0

        spiked = tau1 <=self.delta

        K = spiked.sum()

        spike_increments = ((spiked*-1)+K)/self.N

        avg = self.x.mean()

        junction_increments = self.lambda_junction*(avg-self.x)

        self.x += junction_increments

        leak_increments = self.leak_rate*(-self.x)

        j = np.where(spiked)

        self.x[j] = 0
        self.x+=spike_increments
        self.x+=leak_increments

        return spiked, self.x


class multi_region:

    def __init__(self, N, proportions=[0.1,0.1], weights=[1,-1], nets=[network_leaky,network_leaky]):

        self.regions = []
        self.mf_synaptic_weight = []
        self.samples = [[] for i in range(len(N))]

        for i in range(len(N)):
            self.regions.append(nets[i](N=N[i]))
            self.mf_synaptic_weight.append(weights[i]/N[i])

            for j in range(len(N)): #fixed proportions of out axons for a given region

                self.samples[i].append(np.random.choice([0,1], size=(N[i],N[j]),p=[1-proportions[i],proportions[i]]))

            self.samples.append(np.random.choice([0,1], size=()))

        self.proportions=proportions

        self.Ns = N

    def expo(self, x):  # note parameters
        return np.exp(2 * x) - 1

    def step(self):

        activations = []

        for i in range(len(self.Ns)):
            activations.append(self.regions[i].step()[:])


        for i in range(len(activations)):

            for j in range(len(activations)):
                if i!=j:

                    self.regions[j].x += self.samples[i][j][np.where(activations[i][0])].sum(axis=0)*self.mf_synaptic_weight[i]

        return activations

