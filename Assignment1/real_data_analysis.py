from collections import deque
from heapq import heappush, heappop
import matplotlib.pyplot as plt
from random import expovariate, randint
import csv
from datetime import datetime
from random import randint
import random
import numpy as np

queueLength = []
simulated_delay_list = []
simulated_avg_list = []
NUMBER_SERVER = 50  # number of servers
CHOICE = [1, 2, 5, 10, 30]
supermark = True


class Arrival:
    def __init__(self, arrival_id):
        self.arrival_id = arrival_id

    def __lt__(self, other):
        return True

    def process(self, state):
        groupfifo = {}
        dict_list = random.sample(list(dict.fromkeys(state.fifo)), k=d)
        for dictindex in dict_list:
            groupfifo[dictindex] = len(state.fifo[dictindex])
        fifoindex = min(groupfifo, key=groupfifo.get)
        state.id_list[self.arrival_id] = fifoindex
        state.arrivals[self.arrival_id] = state.t
        state.fifo[fifoindex].append(self.arrival_id)
        for dictindex in range(len(state.fifo)):
            state.fifo_length[dictindex].append(len(state.fifo[dictindex]))


class Completion:
    def __init__(self, completion_id):
        self.completion_id = completion_id

    def __lt__(self, other):
        return True

    def process(self, state):
        if self.completion_id in state.id_list.keys():
            popedid = state.fifo[state.id_list[self.completion_id]].popleft()
            state.completions[self.completion_id] = state.t


class State:
    def __init__(self, start_time, end_time, joibid):
        self.jobid = joibid
        self.t = start_time
        self.fifo = {}
        self.fifo_length = {}
        self.id_list = {}
        for server_number in range(0, NUMBER_SERVER):
            self.fifo_length[server_number] = []
        for server in range(0, NUMBER_SERVER):
            self.fifo[server] = deque()
        self.arrivals = {}  # jobid -> arrival time mapping
        self.completions = {}  # jobid -> completion time mapping
        self.events = [(start_time, Arrival(self.jobid)), (end_time, Completion(self.jobid))]


for d in CHOICE:
    state = None
    delay_time = 0
    avg_length = []
    avgLen = 0
    with open('real_data.csv') as csvfile:
        rows = csv.reader(csvfile)
        for rowid, row in enumerate(rows):
            try:
                if not row[1] or not row[2]:
                    continue
                start_time = datetime.strptime('-'.join(row[1].split('-')[:-1]), '%Y-%m-%d %H:%M:%S').timestamp()
                end_time = datetime.strptime('-'.join(row[2].split('-')[:-1]), '%Y-%m-%d %H:%M:%S').timestamp()
                if not state:
                    state = State(start_time, end_time, rowid)
                else:
                    heappush(state.events, (start_time, Arrival(rowid)))
                    heappush(state.events, (end_time, Completion(rowid)))
            except ValueError:
                print(row)

    while state.events:
        t, event = heappop(state.events)
        state.t = t
        event.process(state)

    for job_id in state.completions:
        delay_time += state.completions[job_id] - state.arrivals[job_id]
    avg_delay_time = delay_time / len(state.completions)
    simulated_delay_list.append(avg_delay_time)

    for queue_length in state.fifo_length.values():
        avg_length.append(sum(queue_length) / len(queue_length))
    avgLen = sum(avg_length) / len(avg_length)
    simulated_avg_list.append(avgLen)
    print(simulated_delay_list, simulated_avg_list)

    y = []
    x = range(1, 15)
    for length in x:
        value = 0
        for queue_value in state.fifo_length.values():
            value += len([i for i in queue_value if i >= length]) / len(queue_value)
        y.append(value / len(state.fifo_length))
    plt.plot(x, y, label=f"Choice {d}")
plt.ylim(0, 1)
plt.ylabel('Fraction of queues with at least that size')
plt.xlabel('Queue length')
plt.legend()
plt.show()
