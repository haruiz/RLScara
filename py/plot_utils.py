import typing

import matplotlib.pyplot as plt
import pandas as pd


def plot_episode_stats(
    episode_lengths: typing.List,
    episode_rewards: typing.List,
    smoothing_window: int = 10,
    title: str = "Episode Statistics",
):
    """
    Plot the episode length over time
    """

    # Plot the episode length over time
    fig = plt.figure(figsize=(10, 5))

    ax = fig.add_subplot(1, 2, 1)
    ax.plot(episode_lengths)
    ax.set_xlabel("Episode")
    ax.set_ylabel("Episode Length")
    ax.set_title("Episode Length over Time")

    # Plot the episode reward over time
    rewards_smoothed = (
        pd.Series(episode_rewards)
        .rolling(smoothing_window, min_periods=smoothing_window)
        .mean()
    )
    ax = fig.add_subplot(1, 2, 2)
    ax.plot(rewards_smoothed)
    ax.set_xlabel("Episode")
    ax.set_ylabel("Episode Reward (Smoothed)")
    ax.set_title(
        "Episode Reward over Time (Smoothed over window size {})".format(
            smoothing_window
        )
    )

    plt.suptitle(title)
    fig.savefig("plot.png")
    plt.show()
