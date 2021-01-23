from network import *
from matplotlib import pyplot as plt

T = 10 #duration of simulation
delta = 0.01 #bin sizes
iterations = int(T/delta)
N=200 #number of neurons

model = network(N=N, delta=delta, lambda_junction=0.02)

spike_train = []
voltages = []
spike_events = [[] for i in range(N)]

for i in range(iterations):

    s, v = model.step()
    spike_train.append(s.copy())
    voltages.append(v.copy())

    for j in np.where(s)[0]: #convert spike into event

        spike_events[j].append(i*delta)


spike_train = np.array(spike_train).transpose() #neuron x time
voltages = np.array(voltages).transpose() #neuron x time

plt.figure(1)
plt.eventplot(spike_events, color='black')
plt.xlabel('time (s)')
plt.ylabel('neuron #')

plt.figure(2)
part = 2
index = 1 #what neuron to print the voltage of
t = np.array([(T/part)*i/int(len(voltages[index])/part) for i in range(int(len(voltages[index])/part))])
plt.plot(t, voltages[index][:int(len(voltages[index])/part)], color='black')
plt.ylabel('voltage')
plt.xlabel('time (s)')

plt.show()
