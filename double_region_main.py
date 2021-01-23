from network import *
from matplotlib import pyplot as plt

T = 10
delta = 0.01
iterations = int(T/delta)
N=[100,200]

model = multi_region(N=N, proportions=[0.1,0.1])

spike_train = [[],[]]
voltages = [[],[]]
spike_events = [[[] for j in range(N[i])] for i in range(len(N))]

for i in range(iterations):

    activations = model.step()

    for j in range(len(N)):
        spike_train[j].append(activations[j][0].copy())
        voltages[j].append(activations[j][1].copy())

        for q in np.where(activations[j][0])[0]:
            spike_events[j][q].append(i * delta)


spike_events = np.array(spike_events)
for i in range(len(voltages)):
    voltages[i] = np.array(voltages[i]).transpose()


for i in range(len(spike_events)):

    plt.figure(2*i+1)
    plt.eventplot(spike_events[i], color='black')
    plt.xlabel('time (s)')
    plt.ylabel('neuron #')

    plt.figure(2*i+2)
    part = 2
    index = 1

    for j in spike_events[i][index]: # add a spike component to the plot

        voltages[i][index][int(j/delta)] = 3

    t = np.array([(T / part) * j / int(len(voltages[i][index]) / part) for j in range(int(len(voltages[i][index]) / part))])
    plt.plot(t, voltages[i][index][-int(len(voltages[i][index]) / part):], color='black')
    plt.ylabel('voltage')
    plt.xlabel('time (s)')


plt.show()