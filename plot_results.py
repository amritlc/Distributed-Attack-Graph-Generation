import pandas as pd
import matplotlib.pyplot as plt


def plot_results():

    df = pd.read_csv("results/experiment_results.csv")

    plt.figure(figsize=(10, 6))

    plt.plot(df["Host Count"], df["Serial DFS Time"], marker="o", label="Serial DFS")
    plt.plot(df["Host Count"], df["Distributed 2 Agents Time"], marker="o", label="Distributed 2 Agents")
    plt.plot(df["Host Count"], df["Distributed 3 Agents Time"], marker="o", label="Distributed 3 Agents")
    plt.plot(df["Host Count"], df["Distributed 4 Agents Time"], marker="o", label="Distributed 4 Agents")

    plt.xlabel("Host Count")
    plt.ylabel("Runtime (seconds)")
    plt.title("Serial vs Simulated Distributed Attack Graph Generation")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig("plots/runtime_comparison.png")
    plt.show()


if __name__ == "__main__":
    plot_results()