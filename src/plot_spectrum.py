#!/usr/bin/env python3


"""
Plot a scan of the average plaquette
"""


from argparse import ArgumentParser

import matplotlib.pyplot as plt
from su2pg_analysis.plots import basic_plot, errorbar_pyerrors


def parse_observable(observable_channel, rescale_w0):
    observable, channel = observable_channel.split("_")
    name = "{channel}_{observable}".format(
        channel=channel,
        observable={"f": "decay_const", "m": "mass"}[observable],
    )
    label = r"${maybe_a}{observable}_{{\mathrm{{{channel}}}}}{maybe_w0}$".format(
        channel=channel.upper(),
        observable=observable,
        maybe_a="" if rescale_w0 else "a",
        maybe_w0="w_0" if rescale_w0 else "",
    )
    return name, label


def zero_axis(ax, x_or_y):
    lower, upper = getattr(ax, f"get_{x_or_y}lim")()
    if lower > 0:
        lower = 0
    if upper < 0:
        upper = 0
    getattr(ax, f"set_{x_or_y}lim")(lower, upper)


def get_ylabel(observables, rescale_w0):
    if len(observables) == 1:
        _, label = parse_observable(observables[0], rescale_w0)
        return label
    elif len(set(observable[0] for observable in observables)) == 1:
        if rescale_w0:
            return f"${observables[0][0]}w_0$"
        else:
            return f"$a{observables[0][0]}$"
    else:
        return "Observable"


def rescale_data(data, name, rescale_w0):
    obs_data = data[name]
    if rescale_w0:
        obs_data = [
            obs_datum * w0_datum
            for obs_datum, w0_datum in zip(obs_data, data["clover_w0"])
        ]
        for datum in obs_data:
            datum.gamma_method()

    return obs_data


def plot(data, x_observable, y_observables, zero_x_axis, zero_y_axis, rescale_w0):
    fig, ax = plt.subplots(layout="constrained")
    if not y_observables:
        y_observables.append("m_v")

    x_name, x_label = parse_observable(x_observable, rescale_w0)
    x_data = rescale_data(data, x_name, rescale_w0)

    markers = "os^v"
    for color_index, (y_observable, marker) in enumerate(zip(y_observables, markers)):
        y_name, y_label = parse_observable(y_observable, rescale_w0)
        y_data = rescale_data(data, y_name, rescale_w0)

        errorbar_pyerrors(
            ax,
            data[x_name],
            data[y_name],
            marker=marker,
            label=y_label,
            color=f"C{color_index}",
        )

    ax.set_xlabel(x_label)
    ax.set_ylabel(get_ylabel(y_observables, rescale_w0))

    if zero_x_axis:
        zero_axis(ax, "x")
    if zero_y_axis:
        zero_axis(ax, "y")

    if len(y_observables) > 1:
        ax.legend(loc="best")

    return fig


if __name__ == "__main__":
    basic_plot(
        plot,
        "Plot one state against another for each ensemble",
        {
            "--x_observable": {
                "help": "Observables to put on the horizontal axis",
                "default": "m_ps",
            },
            "--y_observable": {
                "help": "Observables to put on the vertical axis",
                "action": "append",
            },
            "--zero_x_axis": {
                "help": "Ensure that zero is present on the vertical axis",
                "action": "store_true",
            },
            "--zero_y_axis": {
                "help": "Ensure that zero is present on the vertical axis",
                "action": "store_true",
            },
            "--rescale_w0": {
                "help": "Rescale axes by w_0",
                "action": "store_true",
            },
        }
    )
