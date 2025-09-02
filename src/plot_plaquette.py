#!/usr/bin/env python3


"""
Plot a scan of the average plaquette
"""


from argparse import ArgumentParser

import matplotlib.pyplot as plt
from su2pg_analysis.plots import basic_plot, errorbar_pyerrors


def plot(data):
    fig, ax = plt.subplots(layout="constrained")

    errorbar_pyerrors(
        ax,
        data["beta"],
        data["plaquette"],
        marker="o",
    )
    ax.set_xlabel(r"$\beta$")
    ax.set_ylabel(r"$\langle \mathcal{P} \rangle$")
    return fig


if __name__ == "__main__":
    basic_plot(plot, "Plot a scan of the average plaquette as a function of beta")
