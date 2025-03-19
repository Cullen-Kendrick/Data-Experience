import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random 

import mesa
from mesa import Agent, Model, batch_run
from mesa.time import RandomActivation
from mesa.space import SingleGrid

class SIRAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.health = 'S'
        self.inf_timer = 0
    def infec(self): 
        if self.health == 'S':
            if (random.randrange(0,1000) > 997) == True:
                self.health = 'V'
            else: 
                neighbors = self.model.grid.get_neighbors(self.pos, moore= False)
                if len(neighbors) > 0:
                    for neighbor in neighbors:
                        if neighbor.health == 'I':
                            self.health = 'I'
                            self.model.hchange = True
        if self.health == 'I': 
            self.inf_timer +=1
            if self.inf_timer == self.model.infec_dur -1:
                if random.choice([True, False, False, False, False]) == True:
                    self.health = 'D'
            if self.inf_timer == self.model.infec_dur:
                self.health = 'R'
            if self.inf_timer < self.model.infec_dur: 
                self.model.hchange = True

    def move(self):
        if self.health != 'D':
            pos_steps = self.model.grid.get_neighborhood(self.pos, moore= False)
            place = self.random.choice(pos_steps)
            if self.model.grid.is_cell_empty(place):
                self.model.grid.move_agent(self, place)
    def step(self):
        self.move()
        self.infec()
    
class SIRModel(Model): 
    def __init__(self, num_agents, num_infec, infec_dur, dim):
        super().__init__()
        self.num_agents = num_agents 
        self.dim = dim
        self.num_infec = num_infec
        self.infec_dur = infec_dur
        self.num_vax = round(num_agents/66)
        self.running = True
        self.num_steps = 1
        self.schedule = RandomActivation(self)
        self.time = []
        self.grid = SingleGrid(dim, dim, torus= False)
        for i in range(self.num_agents):
            a = SIRAgent(i, self)
            self.schedule.add(a)
            if self.num_infec > 0:
                a.health = 'I'
                self.num_infec -= 1
            elif self.num_vax > 0: 
                a.health = 'V'
                self.num_vax -= 1
            self.grid.move_to_empty(a)
        self.Sstock = []
        self.Istock = []
        self.Rstock = []
        self.Dstock = []
        self.Vstock = []
    def step(self):
        self.hchange = False
        self.schedule.step()
        self.health_count()
        self.timeline()
        self.display_grid()
        #print(self.hchange)
        if not self.hchange: 
            self.running = False
    def health_count(self):
        self.Sagent = 0
        self.Iagent = 0 
        self.Ragent = 0 
        self.Dagent = 0
        self.Vagent = 0
        for agent in self.schedule.agents: 
            if agent.health == "S":
                agent.model.Sagent += 1 
            if agent.health == "I":
                agent.model.Iagent += 1 
            if agent.health == "R":
                agent.model.Ragent += 1 
            if agent.health == "D":
                agent.model.Dagent +=1 
            if agent.health == 'V':
                agent.model.Vagent += 1
        self.Sstock.append(self.Sagent)
        self.Istock.append(self.Iagent)
        self.Rstock.append(self.Ragent)
        self.Dstock.append(self.Dagent)
        self.Vstock.append(self.Vagent)
    def timeline(self): 
        self.time.append(self.num_steps)
        self.num_steps += 1
    def display_grid(self): 
        cells = np.zeros((self.dim, self.dim))
        for a in self.schedule.agents:
            if a.health == 'S':
                cells[a.pos[0], a.pos[1]] = 1
            elif a.health == "I":
                cells[a.pos[0], a.pos[1]] = 2
            elif a.health == 'R':
                cells[a.pos[0], a.pos[1]] = 3
            elif a.health == 'D':
                cells[a.pos[0], a.pos[1]] = 4 
            elif a.health == 'V':
                cells[a.pos[0], a.pos[1]] = 5
        plt.clf()
        sns.heatmap(cells, cmap= "Purples", vmin= 0, vmax= 5,
                    cbar= True, annot= False, square= True)
        plt.pause(.001)
        plt.show()
        
test = SIRModel(500, 1, 5, 30)
while test.running:
    test.step()

print(test.Vstock)
plt.plot(test.time, test.Sstock, color="blue", label="S")
plt.plot(test.time, test.Istock, color="red", label="I")
plt.plot(test.time, test.Rstock, color="green", label="R")
plt.plot(test.time, test.Dstock, color='black', label='D')
plt.plot(test.time, test.Vstock, color='purple', label='V')
plt.title('Agent Based SIR Model')
plt.legend()
plt.show()