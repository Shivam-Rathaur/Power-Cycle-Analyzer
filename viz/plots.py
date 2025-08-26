# viz/plots.py
import matplotlib.pyplot as plt

def plot_cycle_Ts(states, title="Rankine Cycle (T-s)"):
    s = [states[k].s/1e3 for k in ["1","2","3","4","1"]]
    T = [states[k].T for k in ["1","2","3","4","1"]]
    plt.figure(); plt.plot(s, T, marker="o"); plt.xlabel("s [kJ/kg-K]"); plt.ylabel("T [K]"); plt.title(title); plt.grid(True)

def plot_cycle_hs(states, title="Rankine Cycle (h-s)"):
    s = [states[k].s/1e3 for k in ["1","2","3","4","1"]]
    h = [states[k].h/1e3 for k in ["1","2","3","4","1"]]
    plt.figure(); plt.plot(s, h, marker="o"); plt.xlabel("s [kJ/kg-K]"); plt.ylabel("h [kJ/kg]"); plt.title(title); plt.grid(True)


