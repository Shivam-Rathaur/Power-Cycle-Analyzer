from cycles.rankine import basic_rankine
import numpy as np

P_boiler = 15e6
T_turb_in = 600 + 273.15
P_cond = 10e3
res = basic_rankine(P_boiler, T_turb_in, P_cond, eta_turb=0.88, eta_pump=0.85)
print(res["scalars"])

