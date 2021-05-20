import numpy as np
import matplotlib.pyplot as plt

# parameters
r_crystal = 0.1  # 8 inch diameter
r_feed = 0.006
l_crystal = 0.6

h_melt = 0.02  # approximate value

n_samples = 100  # for function evaluation

# boundary layer
smallest_element=0.0003
layer_thickness=0.007
growth_rate=1.2

# meniscus parameters
beta0_feed = 11  # deg
beta0_crys = 0  # TODO -11 deg
rho_l = 2560 # kg/m^3
alpha = 0.83  # N/m^2
g = 9.81  # m/s^2

# free surface
lc = np.sqrt(alpha/(g*rho_l))  # capillary constant
# at feed
h = lc * np.sqrt(2-2 * np.sin(beta0_feed/360*2*np.pi))  # meniscus height
z = np.linspace(0, h, n_samples)[1:]  # excluding starting point because it's not defined there
r = lc * np.arccosh(2 * lc/z)-lc * np.sqrt(4-z**2/lc**2)
r_meniscus_feed = r - r[-1]  # shift it to zero
z_meniscus_feed = z - z[0]  # shift it to zero
# at crystal
h = lc * np.sqrt(2-2 * np.sin(beta0_crys/360*2*np.pi))  # meniscus height
z = np.linspace(0, h, n_samples)[1:]  # excluding starting point because it's not defined there
r = lc * np.arccosh(2 * lc/z)-lc * np.sqrt(4-z**2/lc**2)
r_meniscus_crys = -r + r[-1]
z_meniscus_crys = -z + z.max()
# resulting free surface
r_fs = np.concatenate([np.flip(r_meniscus_feed) + r_feed, r_meniscus_crys + r_crystal])
z_fs = np.concatenate([np.flip(z_meniscus_feed) + z_meniscus_crys.max(), z_meniscus_crys])
s_fs = np.concatenate(
    [r_fs.reshape((len(r_fs), 1)), z_fs.reshape(len(z_fs), 1)], axis=1
)
# plt.plot(r_fs, z_fs)
# plt.show()

# bottom
r_samples = np.linspace(0, r_crystal, n_samples)
z_samples = 0.6*(r_samples ** 1.7 - r_crystal**1.7)  # this leads to approx. 40 mm interface deflection
s_bt = np.concatenate(
    [r_samples.reshape((n_samples, 1)), z_samples.reshape(n_samples, 1)], axis=1
)

# melting front
r_samples = np.linspace(0, r_feed, n_samples)
z_samples = 70 * (r_samples ** 2 - r_feed ** 2) + s_fs[0, 1]  # this leads to approx 3 mm interface deflection
s_mf = np.concatenate(
    [r_samples.reshape((n_samples, 1)), z_samples.reshape(n_samples, 1)], axis=1
)

# crystal bottom
r_samples = np.linspace(0, r_crystal, n_samples)
z_samples = r_samples ** 1.2 - l_crystal - r_crystal**1.2
s_cr = np.concatenate(
    [r_samples.reshape((n_samples, 1)), z_samples.reshape(n_samples, 1)], axis=1
)
