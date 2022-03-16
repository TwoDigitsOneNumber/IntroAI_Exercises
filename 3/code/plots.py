from math import fabs
import pandas as pd
import matplotlib.pyplot as plt

# read data frames
statistics = ["costs", "total_times", "expanded_states", "generated_states"]

data = {}

# read data
for ind,i in enumerate(statistics):
    data[i] = pd.read_csv(f"3/data/{i}.csv")
    data[i].set_index("problem_size", inplace=True)
    print(data[i])
    data[i].drop("Unnamed: 0", axis=1, inplace=True)
    data[i].plot(title=i, logy=True)
    plt.axvline(15, linestyle="--")
    plt.savefig(f"3/figures/{i}.png")


data["costs"].iloc[:,1:].plot(title=i, logy=False)
plt.axvline(15, linestyle="--")
plt.savefig(f"3/figures/{i}_without_dfs.png")

