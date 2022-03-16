import pandas as pd
import matplotlib.pyplot as plt

# read data frames
statistics = ["costs", "total_times", "expanded_states", "generated_states"]

data = {}

# read data
for i in statistics:
    data[i] = pd.read_csv(f"3/data/{i}.csv")
    data[i].set_index("problem_size", inplace=True)
    print(data[i].columns)
    data[i].drop("Unnamed: 0", axis=1, inplace=True)
    data[i].plot(title=i)
    print(data[i])
    plt.savefig(f"3/figures/{i}.png")

