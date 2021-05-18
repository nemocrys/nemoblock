import numpy as np

r_crystal = 0.4
r_feed = 0.1
n_samples = 100

# bottom
r_samples = np.linspace(0, r_crystal, n_samples)
z_samples = 2.2 * r_samples ** 2
s_bt = np.concatenate(
    [r_samples.reshape((n_samples, 1)), z_samples.reshape(n_samples, 1)], axis=1
)

# free surface
r_samples = np.linspace(r_feed, r_crystal, n_samples)
z_samples = 20 * (r_crystal - r_samples) ** 5 + s_bt[-1, 1]
s_fs = np.concatenate(
    [r_samples.reshape((n_samples, 1)), z_samples.reshape(n_samples, 1)], axis=1
)

# melting front
r_samples = np.linspace(0, r_feed, n_samples)
z_samples = 30 * (r_samples ** 3 - r_feed ** 3) + +s_fs[0, 1]

s_mf = np.concatenate(
    [r_samples.reshape((n_samples, 1)), z_samples.reshape(n_samples, 1)], axis=1
)
