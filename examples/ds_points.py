import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from nemoblock import *

"""

solid and fluid directories were wrong

"""


# mesh sizes
res_d = 38
res_h_crystal = 10
res_h_melt = 14

# geometry

h_phase_if_edges = 0.06
h_phase_if_center = 0.06 # 0.08
h_phase_if_side_mid = 0.06 # 0.07

container_d = 0.2
container_h = 0.12

container_r = container_d / 2

# grading
grad_d_layer_size = 0.012
grad_d_n_cells = 5
grad_d_expansion = 4

grad_melt_bt_size = 0.012
grad_melt_bt_cells = 5
grad_melt_bt_expansion = 4

grad_melt_top_size = 0.012
grad_melt_top_cells = 5
grad_melt_top_expansion = 4


grad_crys_top_size = 0.015
grad_crys_top_cells = 5
grad_crys_top_expansion = 4

# phase interface middle
control_points = [
    [-container_r, h_phase_if_side_mid],
    [-container_r * 0.5, h_phase_if_center],
    [0, h_phase_if_center],
    [container_r * 0.5 * 0.8, h_phase_if_center],
    [container_r, h_phase_if_side_mid],
]
s_ph_mid = b_spline(control_points, plot=False, res=100).T
s_ph_mid = spline(s_ph_mid)

# phase interface outside
control_points = [
    [-container_r, h_phase_if_edges],
    [-container_r * 0.5, h_phase_if_side_mid],
    [0, h_phase_if_side_mid],
    [container_r * 0.5 * 0.8, h_phase_if_side_mid],
    [container_r, h_phase_if_edges],
]
s_ph_side = b_spline(control_points, plot=False, res=100).T
s_ph_side = spline(s_ph_side)
