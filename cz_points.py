import numpy as np
import matplotlib.pyplot as plt


# parameters
r_crucible = 0.2
r_crystal = 0.1
l_crystal = 0.6

h_melt = 0.1  # approximate value

n_samples = 100

# boundary layer
smallest_element=0.0003
layer_thickness=0.007
growth_rate=1.2

# meniscus parameters
beta0 = 11  # deg
rho_l = 2560 # kg/m^3
alpha = 0.83  # N/m^2
g = 9.81  # m/s^2


# free surface
lc = np.sqrt(alpha/(g*rho_l))  # capillary constant
# at feed
h = lc * np.sqrt(2-2 * np.sin(beta0/360*2*np.pi))  # meniscus height
z = np.linspace(0, h, n_samples)[1:]  # excluding starting point because it's not defined there
r = lc * np.arccosh(2 * lc/z)-lc * np.sqrt(4-z**2/lc**2)
r_meniscus = r - r[-1] + r_crystal # shift it to r_crystal
z_meniscus = z - z[0]  # shift it to zero
r_outer_part = np.linspace(r_crucible, r_meniscus[0], endpoint=False)
z_outer_part = np.zeros((len(r_outer_part,)))
r_fs = np.concatenate([r_outer_part, r_meniscus])
z_fs= np.concatenate([z_outer_part, z_meniscus])
s_fs = np.concatenate(
    [r_fs.reshape((len(r_fs), 1)), z_fs.reshape(len(z_fs), 1)], axis=1
)
# plt.plot(r_fs, z_fs)
# plt.show()


# bottom
r_samples = np.linspace(0, r_crucible, n_samples)
z_samples = 1e6 * (r_samples ** 10 - r_crucible**10)
s_bt = np.concatenate(
    [r_samples.reshape((n_samples, 1)), z_samples.reshape(n_samples, 1)], axis=1
)
# plt.plot(r_samples, z_samples)
# plt.show()

# phase interface
r_samples = np.linspace(0, r_crystal, n_samples)
z_samples = -30 * (r_samples ** 3 - r_crystal ** 3) + s_fs[-1, 1]
s_ph = np.concatenate(
    [r_samples.reshape((n_samples, 1)), z_samples.reshape(n_samples, 1)], axis=1
)
# plt.plot(r_samples, z_samples)
# plt.show()

# crystal bottom
r_samples = np.linspace(0, r_crystal, n_samples)
z_samples = -(r_samples ** 1.2 - r_crystal ** 1.2)+ s_fs[-1, 1] + l_crystal
s_cr = np.concatenate(
    [r_samples.reshape((n_samples, 1)), z_samples.reshape(n_samples, 1)], axis=1
)
# plt.plot(r_samples, z_samples)
# plt.show()
