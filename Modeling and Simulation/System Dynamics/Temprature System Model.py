
import numpy as np
import matplotlib.pyplot as plt

delta_x = 1/60   # hour
start_x = 0      # hour
end_x = 48     # hour

x = np.arange(start_x, end_x, delta_x)

smidge = 1       # degF
AC_on = np.empty(len(x), dtype=bool)
AC_power = 10   # degF/hr
thermostat = 72      # degF
outside_temp = 125    # degF
insulation_loss_factor = .2    # (degF/hr)/degF

T = np.zeros(len(x))
T[0] = outside_temp    # degF
AC_on[0] = False

for i in range(1,len(T)):
    
    if T[i-1] < thermostat - smidge  and  AC_on[i-1] == True:
        AC_on[i] = False
        cooling = 0    # degF/hr

    elif T[i-1] > thermostat + smidge  and  AC_on[i-1] == False:
        AC_on[i] = True
        cooling = AC_power                # degF/hr

    else:
        AC_on[i] = AC_on[i-1]

    discrepancy = outside_temp - T[i-1]    # degF   (neg for cold outside)
    leakage = (discrepancy * insulation_loss_factor)    # degF/hr  (pos for)

    T_prime = leakage - cooling
    T[i] = T[i-1] + T_prime * delta_x
    
plt.plot(x, T, color="green", label="room temp")
plt.plot(x, AC_on * 10, color="red", label="A/C")
plt.axhline(outside_temp, color="blue", label="outside temp")
plt.axhline(thermostat, color="black", linestyle="dotted", label="thermostat")
plt.axhline(thermostat + smidge, color="gray", linestyle="dotted")
plt.axhline(thermostat - smidge, color="gray", linestyle="dotted")
plt.title("ckendri2_temp 3")
plt.xlabel('hours') 
plt.ylabel('deg F') 
plt.legend()
plt.show()


print(f"The AC was on {AC_on.mean() * 100:.2f}% of the day.")
