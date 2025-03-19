
import numpy as np
import matplotlib.pyplot as plt
import math

def itox(i):
    return start_x + delta_x * i   # hours

dose = 3 * 325 * 1000    # ug
dose_freq = 2            # hours

delta_x = 5/60   # hours
start_x = 0      # hours
end_x = 48      # hours

x = np.arange(start_x, end_x, delta_x)

half_life = 3.2  # hours
plasma_volume = 3 * 1000   # ml
elimination_constant = math.log(2)/half_life   # 1/hr
print(elimination_constant)
metabolism_constant =  0.5              # 1/hr

D = np.zeros(len(x))     # ug
D[0] = 0 

S = np.zeros(len(x))    # ug
S[0] = dose 

for i in range(1, len(x)): 
    if math.isclose(itox(i) % dose_freq, 0):
        dosage = dose *3    
        metabolism = S[i-1] * metabolism_constant
        S_prime = dosage - metabolism 
        S[i] = S[i-1] + delta_x * S_prime 
    else:
        metabolism = S[i-1] * metabolism_constant
        S_prime = - metabolism 
        S[i] = S[i-1] + delta_x * S_prime 
    

for i in range(1, len(x)):
    elimination = D[i-1] * elimination_constant  # ug/hr
    metabolism = S[i-1] * metabolism_constant
    D_prime = metabolism - elimination  # ug/hr
    D[i] = D[i-1] + delta_x * D_prime

    

plasma_concentration = D / plasma_volume   # array  ug/ml
stomach_concentration = S / plasma_volume 

plt.plot(x, plasma_concentration, label="plasma conc", color="purple")
plt.plot(x, stomach_concentration, label="stomach conc", color="green")
plt.axhline(150, color="blue", label="MEC")
plt.axhline(300, color="red", label="MTC")
plt.legend()
plt.title("ckendri2_drugs 2-2.3")
plt.ylabel("ug/ml")
plt.xlabel("hours")
plt.ylim((0,max(350,plasma_concentration.max())))
plt.show()
