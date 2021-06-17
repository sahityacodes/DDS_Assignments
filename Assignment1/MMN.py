#!/usr/bin/env python3
from collections import deque
from heapq import heappush, heappop
from random import expovariate, randint
import random
import matplotlib.pyplot as plt
MAXT = 1000
LAMBDA = [0.5, 0.9, 0.95, 0.99]
MU = 1
NUMBER_SERVER = 50 # number of servers
CHOICE = [1,2,5,10]
supermark =True
delay_time = []
simulated_delay_list = []
theoretical_delay_time = []
simulated_avg_list = []
theoretical_avg_list = []
avgerror = []
error = []
groupfifo = {}


class Arrival:

    def __init__(self, arrival_id):
        self.arrival_id = arrival_id
        self.arrival_time = 0
        self.service_time = 0

    def process(self, state, arrival_rate):

        state.arrivals[self.arrival_id] = state.t
        self.arrival_time = state.t + expovariate(arrival_rate)
        self.service_time = state.t + expovariate(1)
        if self.service_time > self.arrival_time:
           self.time= self.service_time-self.arrival_time #SJF
        else:
            self.time = 0.00
        if supermark:
            groupfifo = {}
            dict_list = random.sample(list(dict.fromkeys(state.server_queue)), k=d)
            for i in dict_list :
                groupfifo[i] = len(state.server_queue[i])
            index = min(groupfifo, key=lambda k: groupfifo[k])
        else:
            index = random.choice(dict_list)
            # index = randint(0, NUMBER_SERVER - 1) # without choice
        heappush(state.server_queue[index], (self.time, self.arrival_id)) #SJF
        # state.server_queue[index].append(self.arrival_id) #FIFO
        for i in range(len(state.server_queue)):
            state.queues_length[i].append(len(state.server_queue[i]))
        self.arrival_id += 1
        heappush(state.events, (self.arrival_time, Arrival(self.arrival_id)))
        if len(state.server_queue[index]) == 1:
            heappush(state.events, (self.service_time, Completion(index)))


class Completion:
    def __init__(self, fifoindex):
        self.fifoindex = fifoindex
    def process(self, state, lamda):
        popid=heappop(state.server_queue[self.fifoindex]) #SJF
        state.completions[popid[1]] = state.t #SJF
        # popid=state.server_queue[self.fifoindex].popleft() #FIFO
        # state.completions[popid] = state.t #FIFO
        if len(state.server_queue[self.fifoindex]) > 0:
            heappush(state.events, (state.t + expovariate(1), Completion(self.fifoindex)))




class State:
    def __init__(self):
        self.t = 0  # current time in the simulation
        self.server_queue = {}
        self.queues_length={}
        for i in range(0,NUMBER_SERVER):
            self.queues_length[i] = []
        for i in range(0, NUMBER_SERVER):
            # self.server_queue[i] = deque() #FIFO
            self.server_queue[i] = [] #SJF
        self.events=[]
        self.arrivals = {}  # jobid -> arrival time mapping
        self.completions = {}  # jobid -> completion time mapping
        heappush(self.events, (self.t, Arrival(0)))



for d in CHOICE:
    delay_time = []
    simulated_delay_list = []
    theoretical_delay_time = []
    simulated_avg_list = []
    theoretical_avg_list = []
    avgerror = []
    error = []
    groupfifo = {}
    for lamda in LAMBDA:
        state = State()
        events = state.events
        while events:
            t, event = heappop(events)
            if t > MAXT:
                break
            state.t = t
            event.process(state, lamda * NUMBER_SERVER)
        # ---------------------------------------
        theoretical_w = 1 / (1 - lamda)
        theoretical_delay_time.append(theoretical_w)
        # # -----------------------------------------

        delay_time = 0
        for server_q in state.completions:
            delay_time += state.completions[server_q] - state.arrivals[server_q]
        avg_delay_time = delay_time / len(state.completions)
        simulated_delay_list.append(avg_delay_time)
        # ----------------------------------------------------
        avg_lenght = 0
        for queue_length in state.queues_length.values():
            avg_lenght += sum(queue_length) / len(queue_length)
        avg_lenght /= len(state.queues_length)
        simulated_avg_list.append(avg_lenght)
        # -------------------------------------------------
        theoretical_avglen = lamda / (1 - lamda)
        theoretical_avg_list.append(theoretical_avglen)
        # --------------------------------------------------
        AvgrError = abs(avg_lenght - theoretical_avglen) / avg_lenght
        avgerror.append(AvgrError)
        # -----------------
        rError = abs(avg_delay_time - theoretical_w) / avg_delay_time
        error.append(rError)
    #     #     -----------------------
        print("lambda {}".format(lamda))
        print("theoretical AVG delay time in M/M/N queue is: {} ".format(theoretical_w))
        print("simulated AVG delay time in M/M/N queue is: {} ".format(avg_delay_time))
        print("Relative Error between  theoretical_w and simulated : {} ".format(rError))
        print("theoretical AVG length of  queue: {} ".format(theoretical_avglen))
        print("simulated AVG length of  queue: {} ".format(avg_lenght))
        print("Relative Error between  theoretical avg queue lenght and simulated avg queue lenght : {} ".format(AvgrError))
        print("length of arrivals : {}".format(len(state.arrivals)))
        print("length of completions : {} ".format(len(state.completions)))

        print("-----------------------------------------------------------------")
        
        y = []
        x = range(1, 15)
        for length in x:
            value = 0
            for server_q in state.queues_length.values():
                value += len([i for i in server_q if i >= length]) / len(server_q)
            y.append(value / len(state.queues_length))

        plt.plot(x, y, label="Lambda = " + str(lamda))
    # plt.title(f"Choice {d}")
    # plt.ylim(0, 1)
    # plt.ylabel('Fraction of queues with at least that size')
    # plt.xlabel('Queue length')
    # plt.legend()
    # plt.show()

    # plt.plot(LAMBDA, simulated_avg_list, 'b--')
    # plt.plot(LAMBDA, simulated_avg_list, 'bs', label='Simulation avg queue length')
    # plt.plot(LAMBDA, theoretical_avg_list, 'g--')
    # plt.plot(LAMBDA, theoretical_avg_list, 'go', label='Theoretical avg queue length')
    # plt.xlabel('Lambda Value')
    # plt.ylabel('Avg queue length')
    # plt.legend()
    # plt.title("Simulation Vs Theoretical :Avg queue length on M/M/N ")
    # plt.show()

    # plt.plot(LAMBDA, simulated_delay_list, 'b--')
    # plt.plot(LAMBDA, simulated_delay_list, 'bs', label='Simulation delay time')
    # plt.plot(LAMBDA, theoretical_delay_time, 'g--')
    # plt.plot(LAMBDA, theoretical_delay_time, 'go', label='Theoretical delay time')
    # plt.xlabel('Lambda Value')
    # plt.ylabel('delay time (secs)')
    # plt.legend()
    # plt.title("Simulation Vs Theoretical : Avg delay time on M/M/N ")
    # plt.legend()
    # plt.show()
