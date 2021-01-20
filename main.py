from network import *
from matplotlib import pyplot as plt

T = 20
delta = 0.01
iterations = int(T/delta)
N=100

model = network(N=N, delta=delta, lambda_junction=0.05)

spike_train = []
voltages = []
spike_events = [[] for i in range(N)]

for i in range(iterations):

    s, v = model.step()
    spike_train.append(s.copy())
    voltages.append(v.copy())

    for j in np.where(s)[0]:

        spike_events[j].append(i*delta)


spike_train = np.array(spike_train).transpose()
voltages = np.array(voltages).transpose()

plt.eventplot(spike_events)
plt.show()
