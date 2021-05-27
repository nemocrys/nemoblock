import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from nemoblock import *

####################
# parameters
r_crucible = 0.2
r_crystal = 0.1
l_crystal = 0.6
l_conus = 0.1

h_melt = 0.2

n_samples = 100

####################
# boundary layer
smallest_element = 0.0003
layer_thickness = 0.04
growth_rate = 1.2

####################
# meniscus parameters
beta0 = 11  # deg
rho_l = 2560  # kg/m^3
alpha = 0.83  # N/m^2
g = 9.81  # m/s^2

####################
# free surface
lc = np.sqrt(alpha / (g * rho_l))  # capillary constant
# at feed
h = lc * np.sqrt(2 - 2 * np.sin(beta0 / 360 * 2 * np.pi))  # meniscus height
z = np.linspace(0, h, n_samples)[
    1:
]  # excluding starting point because it's not defined there
r = lc * np.arccosh(2 * lc / z) - lc * np.sqrt(4 - z ** 2 / lc ** 2)
r_meniscus = r - r[-1] + r_crystal  # shift it to r_crystal
z_meniscus = z - z[0]  # shift it to zero
r_outer_part = np.linspace(r_crucible, r_meniscus[0], endpoint=False)
z_outer_part = np.zeros(
    (
        len(
            r_outer_part,
        )
    )
)
r_fs = np.concatenate([r_outer_part, r_meniscus])
z_fs = np.concatenate([z_outer_part, z_meniscus])
s_fs = np.concatenate(
    [r_fs.reshape((len(r_fs), 1)), z_fs.reshape(len(z_fs), 1)], axis=1
)

####################
# bottom (crucible)
control_points = [
    [0, -0.2],
    [0.2 * 0.5, -0.2],
    [0.2 * 0.8, -0.2],
    [0.2, -0.15],
    [0.2, 0],
]
s_bt = b_spline(control_points, plot=False, res=n_samples).T

####################
# phase interface
control_points = [
    [0, -0.015],
    [r_crystal * 0.2, -0.015],
    [r_crystal * 0.8, -0.01],
    [r_crystal, 0],
]
s_ph = b_spline(control_points, plot=False, res=n_samples).T
s_ph[:, 1] += s_fs[-1, 1]

####################
# crystal conus
s_cr = np.array(
    [
        [0, l_crystal + l_conus],
        [r_crystal / 3, l_crystal + l_conus * 2 / 3],
        [r_crystal * 2 / 3, l_crystal + l_conus / 3],
        [r_crystal, l_crystal],
    ]
)
s_cr[:, 1] += s_fs[-1, 1]
