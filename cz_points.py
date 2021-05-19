import numpy as np

r_crucible = 0.4
r_crystal = 0.1
n_samples = 100

# bottom
r_samples = np.linspace(0, r_crucible, n_samples)
z_samples = 2.2 * r_samples ** 2
s_bt = np.concatenate(
    [r_samples.reshape((n_samples, 1)), z_samples.reshape(n_samples, 1)], axis=1
)

# free surface
r_samples = np.linspace(r_crystal, r_crucible, n_samples)
z_samples = 20 * (r_crucible - r_samples) ** 5 + s_bt[-1, 1]
s_fs = np.concatenate(
    [r_samples.reshape((n_samples, 1)), z_samples.reshape(n_samples, 1)], axis=1
)

# phase interface
r_samples = np.linspace(0, r_crystal, n_samples)
z_samples = -30 * (r_samples ** 3 - r_crystal ** 3) + s_fs[0, 1]
s_ph = np.concatenate(
    [r_samples.reshape((n_samples, 1)), z_samples.reshape(n_samples, 1)], axis=1
)

# crystal bottom
r_samples = np.linspace(0, r_crystal, n_samples)
z_samples = -r_samples ** 1.2 + 1
s_cr = np.concatenate(
    [r_samples.reshape((n_samples, 1)), z_samples.reshape(n_samples, 1)], axis=1
)
