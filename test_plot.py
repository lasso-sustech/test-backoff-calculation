#!/usr/bin/env python3

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']

x_ticks = [15, 31, 63, 127, 255]

sim_a = [0.46666667, 0.66816510, 0.81122157, 0.89865872, 0.94739614]
sim_b = [0.46666667, 0.28892521, 0.16398126, 0.08792846, 0.04561569]
sim_a1 = [sim_a[i+1]/sim_a[i] for i in range(4)]
sim_b1 = [sim_b[i+1]/sim_b[i] for i in range(4)]

exp_a = [14.5, 18.8, 22.5, 24.8, 25.9] #27.0, 27.3]
exp_b = [13.9, 9.43, 5.68, 3.08, 1.63] #0.86, 0.46]
exp_a1 = [exp_a[i+1]/exp_a[i] for i in range(4)]
exp_b1 = [exp_b[i+1]/exp_b[i] for i in range(4)]

fig, ax = plt.subplots()
ax.set_xlabel('设备B的cw_min')
# ax1 = ax.twinx()

ax.plot(x_ticks, exp_a, '.-r')
ax.plot(x_ticks, exp_b, '.-b')
ax.set_ylabel('平均吞吐量')
ax.legend(['设备 A', '设备 B'], loc=2)

# ax1.plot(x_ticks, sim_a, '.--r')
# ax1.plot(x_ticks, sim_b, '.--b')
# ax1.set_ylabel('Access Probability')
# ax1.legend(['Markov A', ' Markov B'], loc=1)

plt.show()