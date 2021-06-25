from chainconsumer import ChainConsumer
from scipy.stats import norm
import emcee
import matplotlib.pyplot as plt
import numpy as np

num_points = 20
m, c = np.tan(np.pi / 4), -1  # So our angle is 45 degrees, m = 1
np.random.seed(0)
xs = np.random.uniform(size=num_points) * 10 + 2
ys = m * xs + c
err = np.sqrt(ys)
ys += err * np.random.normal(size=num_points)

fig, ax = plt.subplots(figsize=(8,3))
ax.errorbar(xs, ys, yerr=err, fmt='.', label="Observations", ms=5)
ax.legend(frameon=False, loc=2)
ax.set_xlabel("x")
ax.set_ylabel("y");

def log_prior(xs):
    phi, c = xs
    if np.abs(phi) > np.pi / 2:
        return -np.inf
    return 0

def log_likelihood(xs, data):
    phi, c = xs
    xobs, yobs, eobs = data
    model = np.tan(phi) * xobs + c
    diff = model - yobs
    return norm.logpdf(diff / eobs).sum()

def log_posterior(xs, data):
    prior = log_prior(xs)
    if not np.isfinite(prior):
        return prior
    return prior + log_likelihood(xs, data)

ndim = 2  # How many parameters we are fitting. This is our dimensionality.
nwalkers = 50  # Keep this well above your dimensionality.
p0 = np.random.uniform(low=-1.5, high=1.5, size=(nwalkers, ndim))  # Start points
sampler = emcee.EnsembleSampler(nwalkers, ndim, log_posterior, args=[(xs, ys, err)])
state = sampler.run_mcmc(p0, 4000)  # Tell each walker to take 4000 steps
chain = sampler.chain[:, 200:, :]  # Throw out the first 200 steps
flat_chain = chain.reshape((-1, ndim))  # Stack the steps from each walker

c = ChainConsumer()
c.add_chain(flat_chain, parameters=[r"$\phi$", "$c$"], color="b")
c.add_chain(sampler.chain.reshape((-1, ndim)), color="r")
c.plotter.plot_walks(truth=[np.pi/4, -1], figsize=(8,4));

c = ChainConsumer()
c.add_chain(flat_chain, parameters=[r"$\phi$", "$c$"])
c.configure(contour_labels="confidence")
c.plotter.plot(truth=[np.pi/4, -1], figsize=2.0)
summary = c.analysis.get_summary()
for key, value in summary.items():
    print(key, value)

x_vals = np.linspace(2, 12, 30)
# Calculate best fit
phi_best = summary[r"$\phi$"][1]
c_best = summary[r"$c$"][1]
best_fit = np.tan(phi_best) * x_vals + c_best

# Calculate range our uncertainty gives using 2D matrix multplication
realisations = np.tan(flat_chain[:, 0][:, None]) * x_vals + flat_chain[:, 1][:, None]
bounds = np.percentile(realisations, 100 * norm.cdf([-2, -1, 1, 2]), axis=0)

# Plot everything
fig, ax = plt.subplots()
ax.errorbar(xs, ys, yerr=err, fmt='.', label="Observations", ms=5, lw=1)
ax.plot(x_vals, best_fit, label="Best Fit", c="#003459")
ax.plot(x_vals, x_vals - 1, label="Truth", c="k", ls=":", lw=1)
plt.fill_between(x_vals, bounds[0, :], bounds[-1, :],
                 label="95\% uncertainty", fc="#03A9F4", alpha=0.2)
plt.fill_between(x_vals, bounds[1, :], bounds[-2, :],
                 label="68\% uncertainty", fc="#0288D1", alpha=0.4)
ax.legend(frameon=False, loc=2)
ax.set_xlabel("x"), ax.set_ylabel("y"), ax.set_xlim(2, 12);