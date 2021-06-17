#!/usr/bin/env python3
import pandas as pd
from collections import deque,Counter
from heapq import heappush, heappop
from random import expovariate
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

MAXT = 10000000
LAMBDA = [0.5, 0.9, 0.95, 0.99]
MU = 1
queueLength = []
avgqueueLen = []
delay_time = []
simulated_delay_list = []
theoretical_delay_time = []
error=[]
avgerror=[]
simulated_avg_list = []
theoretical_avg_list = []
time=[]

class Arrival:


    def __init__(self, id):
        self.Id = id
        self.arrival_time = 0
        self.service_time = 0

    def process(self, state, arrival_rate):
        queueLength.append(len(state.fifo))
        state.arrivals[self.Id] = state.t
        state.fifo.append(self.Id)
        self.arrival_time = state.t + expovariate(arrival_rate)
        self.service_time = state.t + expovariate(1)
        self.Id += 1
        heappush(state.events, (self.arrival_time, Arrival(self.Id)))
        if len(state.fifo) == 1:
            heappush(state.events, (self.service_time, Completion()))




class Completion:
    def process(self, state, lamda):
        complatedjob = state.fifo.popleft()  # remove the first job from the FIFO queue
        state.completions[complatedjob] = state.t

        if len(state.fifo) > 0:
            heappush(state.events, (state.t + expovariate(1), Completion()))

class State:
    def __init__(self):
        self.t = 0  # current time in the simulation
        self.events = [(self.t, Arrival(0))]  # queue of events to simulate
        self.fifo = deque()  # queue at the server
        self.arrivals = {}  # jobid -> arrival time mapping
        self.completions = {}  # jobid -> completion time mapping


def getCount(listOfElems, cond=None):
    'Returns the count of elements in list that satisfies the given condition'
    if cond:
        count = sum(cond(elem) for elem in listOfElems)
    else:
        count = len(listOfElems)
    return count


for lamda in LAMBDA:
    state = State()

    events = state.events

    while events:
        t, event = heappop(events)
        # print(t)
        if t > MAXT:
            break

        state.t = t
        time.append(state.t)
        event.process(state, lamda)

    theoretical_w = 1 / (1 - lamda)
    theoretical_delay_time.append(theoretical_w)
    #     ----------------------------
    avg_delay_time = 0
    for i in state.completions:
        avg_delay_time += state.completions[i] - state.arrivals[i]
    avg_delay_time /= len(state.completions)
    simulated_delay_list.append(avg_delay_time)
    # -----------------------
    avgqueuelenght = 0
    for i in queueLength:
        avgqueuelenght += i
    avgqueuelenght /= len(queueLength)
    simulated_avg_list.append(avgqueuelenght)
    #     -----------------------
    theoretical_avglen = lamda / (1 - lamda)
    theoretical_avg_list.append(theoretical_avglen)
    #     ------------------
    AvgrError = abs(avgqueuelenght - theoretical_avglen) / avgqueuelenght
    avgerror.append(AvgrError)
    # -----------------
    rError = abs(avg_delay_time - theoretical_w) / avg_delay_time
    error.append(rError)
    #     -----------------------

    print("lambda {}".format(lamda))
    print("theoretical AVG delay time in M/M/1 queue is : {} ".format(theoretical_w))
    print("simulated AVG delay time in M/M/1  queue is  : {} ".format(avg_delay_time))
    print("Relative Error between  theoretical and simulated : {} ".format(rError))
    print("theoretical AVG length of  queue: {} ".format(theoretical_avglen))
    print("simulated AVG length of  queue: {} ".format(avgqueuelenght))
    print("Relative Error between  theoretical avg queue lenght and simulated avg queue lenght : {} ".format(AvgrError))
    print("length of queue: {} ".format(len(queueLength)))
    print("length of arrivals : {}".format(len(state.arrivals)))
    print("length of completions : {} ".format(len(state.completions)))
    # print("summary over time {} ".format((queue_summary_over_time)) )
    print("-----------------------------------------------------------------")
    y = []
    y1 = []
    # initializing numerator
    numer = {idx: 0 for idx in set(queueLength)}

    # initializing denominator
    denom = Counter(queueLength)

    x = range(1, 15)
    for element in x:
        count = getCount(queueLength, lambda x: x >= element)
        fraction = count / len(queueLength)
        y.append(fraction)
        # other way
        # fraction1=denom[element]/len(queueLength)
        # y1.append(fraction1)
    plt.plot(x, y, label=f"Lambda ={lamda} ")

plt.ylim(0, 1)
plt.ylabel('Fraction of queues with at least that size')
plt.xlabel('Queue length')
plt.legend()
plt.show()

plt.plot(LAMBDA,simulated_avg_list, 'b--')
plt.plot( LAMBDA,simulated_avg_list, 'bs', label='Simulation avg queue length')
plt.plot(LAMBDA,theoretical_avg_list,  'g--')
plt.plot(LAMBDA,theoretical_avg_list,  'go', label='Theoretical avg queue length')
plt.xlabel('Lambda Value')
plt.ylabel('Avg queue length')
plt.legend()
plt.title("Simulation Vs Theoretical :Avg queue length on M/M/1 ")
plt.show()

print(simulated_delay_list)
print(theoretical_delay_time)
plt.plot(LAMBDA,simulated_delay_list, 'b--')
plt.plot( LAMBDA,simulated_delay_list, 'bs', label='Simulation delay time')
plt.plot(LAMBDA,theoretical_delay_time,  'g--')
plt.plot(LAMBDA,theoretical_delay_time,  'go', label='Theoretical delay time')
plt.xlabel('Lambda Value')
plt.ylabel('delay time (secs)')
plt.legend()
plt.title("Simulation Vs Theoretical : Avg delay time on M/M/1 ")
plt.show()
