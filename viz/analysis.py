import pandas as pd, seaborn as sns, matplotlib.pyplot as plt

def plot_efficiency_heatmap(df):
    pivot_table = df.pivot(index="T_turb_in_C", columns="P_boiler_MPa", values="eta_th")
    plt.figure(figsize=(8,6))
    sns.heatmap(pivot_table, cmap="viridis", annot=False)
    plt.title("Rankine Cycle Efficiency (%)")
    plt.xlabel("Boiler Pressure [MPa]")
    plt.ylabel("Turbine Inlet Temp [°C]")
    plt.show()
