"""Estimate pi by Monte Carlo sampling.

Throw N random darts at the unit square; the fraction that lands inside
the quarter circle approximates pi/4. The RNG seed is fixed, so the same
locked environment produces the identical figure and numbers anywhere.
"""

import argparse

import matplotlib

matplotlib.use("Agg")  # render without a display (JupyterHub terminal, CI)
import matplotlib.pyplot as plt
import numpy as np

SEED = 42


def estimate_pi(n_samples, rng):
    xy = rng.random((n_samples, 2))
    inside = (xy**2).sum(axis=1) <= 1.0
    running = 4 * np.cumsum(inside) / np.arange(1, n_samples + 1)
    return xy, inside, running


def plot(xy, inside, running, out="pi-estimate.png"):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
    n_show = min(len(xy), 5000)  # keep the scatter readable
    pts, hit = xy[:n_show], inside[:n_show]
    ax1.scatter(*pts[hit].T, s=4, label="inside")
    ax1.scatter(*pts[~hit].T, s=4, label="outside")
    ax1.set(title=f"First {n_show:,} darts", xlabel="x", ylabel="y", aspect="equal")
    ax1.legend(loc="lower left")
    ax2.plot(running, lw=1)
    ax2.axhline(np.pi, color="tab:red", ls="--", label="true π")
    ax2.set(title="Running estimate", xlabel="darts thrown", ylabel="estimate of π")
    ax2.set_ylim(3.0, 3.3)
    ax2.legend()
    fig.tight_layout()
    fig.savefig(out, dpi=150)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=100_000)
    args = parser.parse_args()
    rng = np.random.default_rng(SEED)
    xy, inside, running = estimate_pi(args.samples, rng)
    estimate = running[-1]
    error = abs(estimate - np.pi)
    print(f"samples : {args.samples:,}")
    print(f"estimate: {estimate:.6f}")
    print(f"error   : {error:.6f} ({100 * error / np.pi:.4f}%)")
    plot(xy, inside, running)
    print("wrote   : pi-estimate.png")


if __name__ == "__main__":
    main()
