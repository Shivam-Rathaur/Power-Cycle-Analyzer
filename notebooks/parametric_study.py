import numpy as np, pandas as pd
import seaborn as sns, matplotlib.pyplot as plt
from cycles.rankine import basic_rankine

P_boilers = np.linspace(8e6, 22e6, 8)
T_inlets  = np.linspace(500+273.15, 650+273.15, 8)
P_cond    = 8e3

results = []
for Pb in P_boilers:
    for Tin in T_inlets:
        out = basic_rankine(Pb, Tin, P_cond, eta_turb=0.88, eta_pump=0.85)
        results.append({
            "P_boiler_MPa": Pb/1e6,
            "T_turb_in_C": Tin-273.15,
            "eta_th": out["scalars"]["eta_th"]*100
        })

df = pd.DataFrame(results)
pivot_table = df.pivot(index="T_turb_in_C", columns="P_boiler_MPa", values="eta_th")

plt.figure(figsize=(8,6))
sns.heatmap(pivot_table, cmap="viridis", annot=False)
plt.title("Rankine Cycle Efficiency (%)")
plt.xlabel("Boiler Pressure [MPa]")
plt.ylabel("Turbine Inlet Temp [°C]")
plt.show()


from viz.analysis import plot_efficiency_heatmap
plot_efficiency_heatmap(df)
