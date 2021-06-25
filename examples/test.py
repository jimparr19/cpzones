import numpy as np

# prior information
race_weight = 70
race_distance = 5000
race_time = 1200

air_density = 1.225

fatigue_factor = np.array([1.05, 1.08])  # Amount a runner's velocity decreases as race distance increases.
c = np.array([0.88, 1.08])  # specific energy cost of running (related to running economy)
cda = np.array([0.2, 0.24])  # coefficient of drag times ares

distance_at_ftp = (3600 / race_time) ** (1 / fatigue_factor) * race_distance
velocity_at_ftp = distance_at_ftp / 3600

power_ftp_upper = min(6.4 * race_weight, (max(c) * max(velocity_at_ftp) * race_weight) + (
        0.5 * air_density * max(cda) * max(velocity_at_ftp) ** 3))  # 6.4 watts/kg is limits of human power
power_ftp_lower = (min(c) * min(velocity_at_ftp) * race_weight) + (
        0.5 * air_density * min(cda) * min(velocity_at_ftp) ** 3)

race_velocity = race_distance / race_time
race_power_upper = (max(c) * race_velocity * race_weight) + (0.5 * air_density * max(cda) * race_velocity ** 3)
race_power_lower = (min(c) * race_velocity * race_weight) + (0.5 * air_density * min(cda) * race_velocity ** 3)

# wprime_l = (race_power_upper - power_ftp_upper) * race_time
# wprime_u = (race_power_lower - power_ftp_lower) * race_time

wprime_l = 10000
wprime_u = 30000

wprime_truth = (wprime_l + wprime_u) / 2
power_ftp_truth = (power_ftp_upper + power_ftp_lower) / 2

np.array([race_power_lower, race_power_upper]) * race_time - (power_ftp_upper * race_time)

# linear regression
from scipy.stats import norm


def log_prior(xs):
    theta0, theta1 = xs
    if ((theta0 > wprime_l) and (theta0 < wprime_u)) and ((theta1 > power_ftp_lower) and (theta1 < power_ftp_upper)):
        return 0
    else:
        return -np.inf


def log_likelihood(xs, data):
    theta0, theta1 = xs
    xobs, yobs, eobs = data
    model = theta0 + theta1 * xobs
    diff = model - yobs
    return norm.logpdf(diff / eobs).sum()


def log_posterior(xs, data):
    prior = log_prior(xs)
    if not np.isfinite(prior):
        return prior
    return prior + log_likelihood(xs, data)


import emcee

ndim = 2  # How many parameters we are fitting. This is our dimensionality.
nwalkers = 2 * ndim  # Keep this well above your dimensionality.

p0 = np.random.uniform(low=[wprime_l, power_ftp_lower], high=[wprime_u, power_ftp_upper], size=(nwalkers, ndim))

xs = np.array([120, 600, 1200])
ys = np.array([15000, 21000, 25000]) + np.array([250, 350, 260]) * xs
err = ys * 0.05 * np.ones(len(xs))

# xs = np.array([120])
# ys = np.array([21000]) + np.array([276]) * xs
# err = ys * 0.1 * np.ones(len(xs))

# xs = np.array([120, 600])
# ys = np.array([21000, 21000]) + np.array([276, 276]) * xs
# err = ys * 0.1 * np.ones(len(xs))

# Start points
sampler = emcee.EnsembleSampler(nwalkers, ndim, log_posterior, args=[(xs, ys, err)])
state = sampler.run_mcmc(p0, 4000)  # Tell each walker to take 4000 steps
chain = sampler.chain[:, 200:, :]  # Throw out the first 200 steps
flat_chain = chain.reshape((-1, ndim))  # Stack the steps from each walker

import matplotlib.pyplot as plt

from chainconsumer import ChainConsumer

plt.figure()
c = ChainConsumer()
c.add_chain(flat_chain, parameters=[r"$\theta_0$", r"$\theta_1$"], color="b")
c.add_chain(sampler.chain.reshape((-1, ndim)), color="r")
c.plotter.plot_walks(figsize=(8, 4))

plt.show()

# import matplotlib.pyplot as plt
#
# max_duration = 3600
#
# plt.plot(xs, ys, 'o')
# work_done_duration = np.linspace(0, 3600, 100)
# for i in range(len(flat_chain)):
#     plt.plot(work_done_duration, flat_chain[i, 0] + work_done_duration * flat_chain[i, 1], alpha=0.2, color='black')
#
# plt.show()

plt.figure()
c = ChainConsumer()
c.add_chain(flat_chain, parameters=[r"$\theta_0$", r"$\theta_1$"])
c.configure(contour_labels="confidence")
c.plotter.plot(figsize=2.0)
summary = c.analysis.get_summary()
for key, value in summary.items():
    print(key, value)

plt.show()

# plot grphs
x_vals = np.linspace(0, 3600, 30)
# Calculate best fit
theta0_best = summary[r"$\theta_0$"][1]
theta1_best = summary[r"$\theta_1$"][1]
best_fit = theta0_best + theta1_best * x_vals

# Calculate range our uncertainty gives using 2D matrix multplication
realisations = flat_chain[:, 0][:, None] + x_vals * flat_chain[:, 1][:, None]
bounds = np.percentile(realisations, 100 * norm.cdf([-2, -1, 1, 2]), axis=0)

# Plot everything
fig, ax = plt.subplots()
ax.errorbar(xs, ys, yerr=err, fmt='.', label="Observations", ms=5, lw=1)
ax.plot(x_vals, best_fit, label="Best Fit", c="#003459")
plt.fill_between(x_vals, bounds[0, :], bounds[-1, :],
                 label="95\% uncertainty", fc="#03A9F4", alpha=0.2)
# plt.fill_between(x_vals, bounds[1, :], bounds[-2, :],
#                  label="68\% uncertainty", fc="#0288D1", alpha=0.4)
ax.legend(frameon=False, loc=2)
ax.set_xlabel("x"), ax.set_ylabel("y"), ax.set_xlim(0, 3600)
plt.show()

print(f'cp lower {np.percentile(flat_chain[:, 1], 5)} cp upper {np.percentile(flat_chain[:, 1], 95)}')