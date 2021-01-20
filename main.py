from network import *
from matplotlib import pyplot as plt

T = 30
delta = 0.01
iterations = int(T/delta)
N=50

model = network_leaky(N=N, delta=delta, lambda_junction=0.01, leak_rate=0.04)

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

plt.figure(1)
plt.eventplot(spike_events, color='black')
plt.xlabel('time (s)')
plt.ylabel('neuron #')

plt.figure(2)
part = 2
index = 1
t = np.array([(T/part)*i/int(len(voltages[index])/part) for i in range(int(len(voltages[index])/part))])
plt.plot(t, voltages[index][:int(len(voltages[index])/part)], color='black')
plt.ylabel('voltage')
plt.xlabel('time (s)')

plt.show()
