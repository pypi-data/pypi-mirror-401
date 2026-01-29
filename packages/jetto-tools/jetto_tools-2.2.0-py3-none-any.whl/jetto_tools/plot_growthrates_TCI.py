#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, re, argparse
import numpy as np
import matplotlib.pyplot as plt

__all__ = ["plot_growthrates_TCI"]

def plot_growthrates_TCI(jsp, time, xrhos, kygrid_range, output):
    """
    Parameters
    ----------
    jsp : dyct
        Python dictionary containing JSP output
    xrhos : list of float
        Desired rho_tor_norm values (e.g., [0.9, 0.6, 0.3]).
    time : float
        Single time (e.g., 54.5) at which to extract spectra.
    kygrid_range : list of float
        Range for plotting (e.g. [0, 1]).
    output : str
        Output directory where to save the figure.
    """

    # --- Time and radial grids ---
    tvec = jsp["TIME"]
    #Use the XVEC2 vector to have the correct number of x_points as GA, FK, FR
    xvec = jsp["XVEC2"]
    if time == -1:
        t_idx = -1
    else:
        t_idx = np.argmin(np.abs(tvec - time))
    t_selected = float(tvec[t_idx])
    print(f" Closest time index: {t_selected:.3f} s (requested {time})")

    # --- Identify GA/FR/FK fields ---
    jsp_fields = list(jsp.keys())
    ga_fields = sorted([f for f in jsp_fields if re.match(r"^GA\d+$", f)])
    fr_fields = sorted([f for f in jsp_fields if re.match(r"^FR\d+$", f)])
    fk_fields = sorted([f for f in jsp_fields if re.match(r"^FK\d+$", f)])

    # --- Check that at least GA02, FR02, FK02 exist ---
    required_fields = ["GA02", "FR02", "FK02"]
    missing_fields = [f for f in required_fields if f not in jsp.keys()]
    if missing_fields:
        raise KeyError(f"❌ Missing required fields in JETTO output: {', '.join(missing_fields)}")

    # --- Compute radial indices for all xrhos ---
    x_indices = np.array([np.argmin(np.abs(xvec - xrho)) for xrho in xrhos])

    # --- Preallocate matrices ---
    n_rhos = len(xrhos)
    n_ky = len(fk_fields)
    GA_mat = np.zeros((n_rhos, n_ky))
    FR_mat = np.zeros((n_rhos, n_ky))
    FK_mat = np.zeros((n_rhos, n_ky))

    # --- Stack arrays for each field type ---
    ga_stack = np.array([jsp[f] for f in ga_fields])  # shape: (n_ky, n_time, n_x)
    fr_stack = np.array([jsp[f] for f in fr_fields])
    fk_stack = np.array([jsp[f] for f in fk_fields])

    # --- Extract values for the selected time ---
    ga_t = ga_stack[:, t_idx, :]  # shape: (n_ky, n_x)
    fr_t = fr_stack[:, t_idx, :]
    fk_t = fk_stack[:, t_idx, :]

    # --- Fill matrices by advanced indexing ---
    GA_mat = ga_t[:, x_indices].T  # transpose to shape (n_rhos, n_ky)
    FR_mat = fr_t[:, x_indices].T
    FK_mat = fk_t[:, x_indices].T

    print("\n Data matrices constructed successfully.")
    print(f"GA_mat shape: {GA_mat.shape}")
    print(f"FR_mat shape: {FR_mat.shape}")
    print(f"FK_mat shape: {FK_mat.shape}")

    # === Plotting ===
    fig, axes = plt.subplots(n_rhos, 2, figsize=(10, 4 * n_rhos))
    fig.suptitle(f"@ t={t_selected:.3f} s", fontsize=14)

    for irho, xrho in enumerate(xrhos):
        # Extract corresponding row for this rho
        fk_vals = FK_mat[irho, :]
        ga_vals = GA_mat[irho, :]
        fr_vals = FR_mat[irho, :]

        # --- Plot growth rate ---
        ax_gamma = axes[irho, 0] if n_rhos > 1 else axes[0]
        ax_freq  = axes[irho, 1] if n_rhos > 1 else axes[1]

        ax_gamma.set_xscale("log")
        ax_gamma.set_yscale("log")
        ax_gamma.set_xlim(kygrid_range)
        ax_gamma.set_ylabel(r"$\gamma_{GB}$")

        #  Only show x-axis label for bottom row
        if irho == n_rhos - 1:
            ax_gamma.set_xlabel(r"$k_\theta \rho_s$")

        #  Plot unconnected points
        ax_gamma.plot(fk_vals, ga_vals, "o", color="red")

        #  Internal box label for rho=xrho
        ax_gamma.text(
            0.95, 0.9, rf"$\rho = {xrho}$",
            transform=ax_gamma.transAxes,
            fontsize=10,
            ha="right", va="top",
            bbox=dict(facecolor="white", alpha=0.6, edgecolor="none"))

        # --- Plot frequency ---
        ax_freq.set_xscale("log")
        ax_freq.set_xlim(kygrid_range)
        ax_freq.axhline(0, color="k", linestyle="--", linewidth=0.8)
        ax_freq.set_ylabel(r"$\omega_{GB}$")

        #  Only show x-axis label for bottom row
        if irho == n_rhos - 1:
            ax_freq.set_xlabel(r"$k_\theta \rho_s$")

        #  Plot unconnected points
        ax_freq.plot(fk_vals, fr_vals, "s", color="blue")

        #  Internal box label for rho
        ax_freq.text(
            0.95, 0.9, rf"$\rho = {xrho}$",
            transform=ax_freq.transAxes,
            fontsize=10,
            ha="right", va="top",
            bbox=dict(facecolor="white", alpha=0.6, edgecolor="none"))

    fig.tight_layout()
    fig.subplots_adjust(top=0.92, bottom=0.08)
    # save figure if output path directory is given
    if output:
        os.makedirs(output, exist_ok=True)
        out_path = os.path.join(output, f"tci_plot_t{t_selected:.3f}.png")
        plt.savefig(out_path, dpi=300, bbox_inches="tight")
        print(f"\n💾 Figure saved to: {out_path}")

    return fig

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot TCI growth rates and frequencies for a single JETTO run.")
    parser.add_argument("--jetto_path", default="./", help="Path to the JETTO run directory. Default: current directory.")
    parser.add_argument("-t", "--time", type=float, default=-1, help="Time to plot. Default: take the last time available.")
    parser.add_argument("--xrhos", type=str, default="0.2,0.4,0.6,0.8", help="Comma-separated list of rho values. Default: 0.2,0.4,0.6,0.8.")
    parser.add_argument("--kygrid_range", type=str, default="0.1,50", help="Min,max range of k_theta*rho_s to plot. Default: 0.1,50")
    parser.add_argument("-o", "--output", type=str, default=None, help="Optional output directory to save the figure.")
    args = parser.parse_args()

    xrhos = [float(x.strip()) for x in args.xrhos.split(",")]
    kygrid_range = [float(x.strip()) for x in args.kygrid_range.split(",")]

    # --- Load JETTO run ---
    from jetto_tools.jintrac import jintrac
    print(f"📂 Loading JINTRAC run from: {args.jetto_path}")
    jet = jintrac(
        database="jet",
        nshot=0,
        run=0,
        jetto_path=args.jetto_path,
        data_version="3.39.0",
        backend="std",
        out_memory=True)
    data = jet.jet

    figure = plot_growthrates_TCI(jsp=data,
        xrhos=xrhos,
        time=args.time,
        kygrid_range=kygrid_range,
        output=args.output)
    plt.show()
