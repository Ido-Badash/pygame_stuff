from __future__ import annotations

from typing import Sequence

import matplotlib.pyplot as plt


def plot_speed(
    speeds: Sequence[float],
    title: str = "Player Speed",
    show: bool = True,
    save_path: str | None = None,
) -> None:
    """Plot player speeds over time with minimal matplotlib code.

    - speeds: a list/sequence of speed samples
    - title: chart title
    - show: whether to display the chart (blocking)
    - save_path: optional path to save the figure (PNG)
    """
    if not speeds:
        print("No speeds to plot.")
        return

    plt.figure(figsize=(8, 3))
    plt.plot(speeds, lw=1.5, color="#1f77b4")
    plt.xlabel("Frame")
    plt.ylabel("Speed (px/s)")
    plt.title(title)
    plt.grid(True, alpha=0.25)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Saved plot to {save_path}")

    if show:
        plt.show()
