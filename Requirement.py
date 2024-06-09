import matplotlib.pyplot as plt
from enum import Enum
from utility import solve_quadratic
import numpy as np
from itertools import cycle
from math import sqrt

class RequirementType(Enum):
    STALL_SPEED = "stall speed"
    TAKEOFF_DISTANCE = "takeoff distance"
    LANDING_DISTANCE = "landing distance"


class Requirement():

    def __init__(self, requirements):
        self.requirements = requirements 
            
    def loadings_plot(self, min_w_s=5, max_w_s=100, step=1) -> None:
        W_S_range = np.linspace(min_w_s, max_w_s, int((max_w_s - min_w_s) / step) + 1)
        plt.figure()

        colors = cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k'])

        for requirement in self.requirements:
            color = next(colors)
            if requirement['type'] == RequirementType.STALL_SPEED:
                stall_speed_sizing_wl = self.stall_speed_sizing(
                    requirement['stall speed'],
                    requirement['density'], requirement['C_L_max']
                )
                plt.axvline(x=stall_speed_sizing_wl, label=requirement['name'], color=color)

            elif requirement['type'] == RequirementType.TAKEOFF_DISTANCE:
                takeoff_distance = self.FAR23_takeoff_distance_sizing(
                    requirement['takeoff distance'], requirement['sigma'],
                    requirement['C_L_max_TO'], W_S_range
                )
                if takeoff_distance:
                    plt.plot(W_S_range, takeoff_distance, label=requirement['name'], color=color)
            
            elif requirement['type'] == RequirementType.LANDING_DISTANCE:
                stall_speed_sizing_wl = self.FAR23_landing_distance_sizing(
                    requirement['landing distance'], requirement['density'], requirement['C_L_max_L'],
                    requirement['takeoff weight ratio']
                )
                plt.axvline(x=stall_speed_sizing_wl, label=requirement['name'], color=color)

        plt.legend()
        plt.grid(True)
        plt.xlabel('Wing Loading (W/S)')
        plt.ylabel('Power Loading (W/P)')
        plt.title('Wing Loading vs Power Loading')
        plt.show()

    def stall_speed_sizing(self, stall_speed, density, C_L_max):
        return (stall_speed ** 2 * density * C_L_max) / 2

    def FAR23_takeoff_distance_sizing(self, s_to, sigma, C_L_max_TO, W_S_range):
        results = []
        TOP23 = solve_quadratic(a=0.0149, b=8.134, c=-s_to, name=f'Takeoff distance {s_to}ft')
        
        for W_S in W_S_range:
            W_P = TOP23 * sigma * C_L_max_TO / W_S
            results.append(W_P)

        return results

    def FAR23_landing_distance_sizing(self, landing_distance, density, C_L_max_L, takeoff_weight_ratio):
        v_s_L = sqrt(landing_distance / 0.5136)
        w_s_L = (v_s_L ** 2 * density * C_L_max_L) / 2
        return w_s_L / takeoff_weight_ratio