# cycles/rankine.py
from dataclasses import dataclass
import numpy as np
from typing import Dict
from CoolProp.CoolProp import PropsSI

WATER = "Water"

@dataclass
class State:
    P: float  # Pa
    T: float  # K
    h: float  # J/kg
    s: float  # J/kg/K
    x: float | None = None  # quality if two-phase, else None

def state_PT(P, T, fluid=WATER):
    h = PropsSI("H","P",P,"T",T,fluid)
    s = PropsSI("S","P",P,"T",T,fluid)
    return State(P,T,h,s,None)

def state_Px(P, x, fluid=WATER):
    # for saturated mixes where quality is known
    T = PropsSI("T","P",P,"Q",x,fluid)
    h = PropsSI("H","P",P,"Q",x,fluid)
    s = PropsSI("S","P",P,"Q",x,fluid)
    return State(P,T,h,s,x)

def pump_isentropic(s_in, P_out, fluid=WATER):
    # Find outlet state at s_out = s_in, P = P_out (use S,P)
    T_out = PropsSI("T","P",P_out,"S",s_in,fluid)
    h_out = PropsSI("H","P",P_out,"S",s_in,fluid)
    return T_out, h_out

def turbine_isentropic(s_in, P_out, fluid=WATER):
    T_out = PropsSI("T","P",P_out,"S",s_in,fluid)
    h_out = PropsSI("H","P",P_out,"S",s_in,fluid)
    return T_out, h_out

def basic_rankine(P_boiler, T_turb_in, P_cond, eta_turb=1.0, eta_pump=1.0, fluid=WATER) -> Dict:
    # State 1: condenser outlet (sat. liquid)
    s1 = state_Px(P_cond, 0.0, fluid)

    # 1 -> 2: pump to boiler pressure
    T2s, h2s = pump_isentropic(s1.s, P_boiler, fluid)
    h2 = s1.h + (h2s - s1.h)/eta_pump
    s2 = State(P_boiler, T2s, h2, PropsSI("S","P",P_boiler,"H",h2,fluid))

    # 2 -> 3: boiler to superheated at turbine inlet
    s3 = state_PT(P_boiler, T_turb_in, fluid)

    # 3 -> 4: turbine to condenser pressure
    T4s, h4s = turbine_isentropic(s3.s, P_cond, fluid)
    h4 = s3.h - eta_turb*(s3.h - h4s)
    s4 = State(P_cond, T4s, h4, PropsSI("S","P",P_cond,"H",h4,fluid))

    # Energy balance (per kg)
    w_pump = s2.h - s1.h
    q_in   = s3.h - s2.h
    w_turb = s3.h - s4.h
    w_net  = w_turb - w_pump
    eta    = w_net / q_in

    states = {"1": s1, "2": s2, "3": s3, "4": s4}
    scalars = {"w_pump": w_pump, "q_in": q_in, "w_turb": w_turb, "w_net": w_net, "eta_th": eta}
    return {"states": states, "scalars": scalars}

