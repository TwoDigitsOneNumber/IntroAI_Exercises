from cmath import cos
from breadth_first_search import BreadthFirstSearch
from contextlib import contextmanager
from depth_first_search import DepthFirstSearch
from pancake_problem import PancakeProblem
import signal
from weighted_astar_search import WeightedAStarSearch
import numpy as np
import pandas as pd

SIMPLE_PANCAKE_PROBLEMS = [
  (1, 5, 6, 2, 4, 3),
  (4, 1, 2, 5, 7, 3, 6),
  (6, 4, 3, 8, 7, 1, 2, 5),
  (7, 9, 8, 6, 1, 2, 5, 3, 4),
  (7, 8, 4, 1, 2, 9, 3, 6, 5, 10),
]

HARD_PANCAKE_PROBLEMS = [
  (10, 12, 7, 16, 4, 8, 1, 13, 18, 5, 15, 2, 20, 6, 17, 3, 9, 14, 11, 19),
  (14, 4, 3, 19, 13, 17, 16, 26, 2, 8, 28, 24, 9, 21, 12, 11, 25, 18, 5,
    15, 20, 23, 29, 10, 30, 7, 27, 22, 6, 1),
  (17, 29, 22, 16, 40, 20, 3, 10, 24, 36, 13, 30, 38, 34, 4, 26, 19, 7,
    21, 28, 25, 2, 8, 11, 35, 37, 15, 6, 27, 18, 31, 12, 33, 14, 23, 5,
    39, 1, 9, 32),
  (29, 38, 20, 32, 41, 43, 7, 39, 26, 13, 14, 1, 31, 5, 27, 35, 10, 21,
    2, 33, 6, 24, 23, 3, 45, 4, 16, 15, 30, 25, 11, 19, 12, 28, 8, 17,
    18, 9, 44, 34, 37, 36, 40, 42, 22),
  (32, 41, 44, 23, 33, 1, 28, 39, 10, 48, 34, 7, 21, 50, 27, 37, 30, 8,
    18, 31, 40, 5, 22, 17, 38, 43, 14, 47, 15, 3, 6, 4, 19, 49, 9, 16,
    35, 2, 20, 25, 36, 42, 13, 29, 45, 46, 24, 12, 11, 26),
]




def run_uninformed_searches(problem, i):
  print("\nDepth-first search:")
  dfs = DepthFirstSearch(problem, print_statistics=True)
  algo_name, cost, total_time, expanded, generated = dfs.run()

  # store data in arrays
  costs[i, 0] = cost
  total_times[i, 0] = total_time
  expanded_states[i, 0] = expanded
  generated_states[i, 0] = generated
  columns[0] = algo_name

  print("\nBreadth-first search:")
  bfs = BreadthFirstSearch(problem, print_statistics=True)
  algo_name, cost, total_time, expanded, generated = bfs.run()

  # store data in arrays
  costs[i, 1] = cost
  total_times[i, 1] = total_time
  expanded_states[i, 1] = expanded
  generated_states[i, 1] = generated
  columns[1] = algo_name


class TimeLimitExceededError(Exception):
  pass


def run_informed_searches(problem, i):
  @contextmanager
  def time_limit(seconds):
    def signal_handler(signum, frame):
      raise TimeLimitExceededError

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
      yield
    finally:
      signal.alarm(0)

  for a_ind, w in enumerate([1, 1.2, 1.5, 2]):
    print(f"\nWeighted A* Search with w={w}:")
    try:
      with time_limit(180):
        wastar = WeightedAStarSearch(problem, w, print_statistics=True)
        algo_name, cost, total_time, expanded, generated = wastar.run()

        # store data in arrays
        costs[i, a_ind+2] = cost
        total_times[i, a_ind+2] = total_time
        expanded_states[i, a_ind+2] = expanded
        generated_states[i, a_ind+2] = generated
        columns[a_ind+2] = algo_name

    except TimeLimitExceededError as e:
      print("Exceeded time limit of 3 minutes...")





# ============================================================

# arrays for storing the performances of the search algorithms (rows: problem_size, columns: algorithms)

# row indices
all_problem_lengths = [len(i) for i in SIMPLE_PANCAKE_PROBLEMS]
all_problem_lengths.extend([len(i) for i in HARD_PANCAKE_PROBLEMS])
n_total = len(all_problem_lengths)

# column names
columns = 6*[np.nan]

# statistics
costs = np.full((n_total, 6), np.nan)
total_times = np.full((n_total, 6), np.nan)
expanded_states = np.full((n_total, 6), np.nan)
generated_states = np.full((n_total, 6), np.nan)




for i, init in enumerate(SIMPLE_PANCAKE_PROBLEMS):
  problem = PancakeProblem(init)
  problem.dump()

  run_uninformed_searches(problem, i)
  run_informed_searches(problem, i)
  print("----------")

for i, init in enumerate(HARD_PANCAKE_PROBLEMS):
  problem = PancakeProblem(init)
  problem.dump()

  i += len(SIMPLE_PANCAKE_PROBLEMS)

  run_informed_searches(problem, i)
  print("----------")


# convert all arrays to dataframes
costs = pd.DataFrame(costs)
total_times = pd.DataFrame(total_times)
expanded_states = pd.DataFrame(expanded_states)
generated_states = pd.DataFrame(generated_states)


# set indices and column names
costs.columns = columns
total_times.columns = columns
expanded_states.columns = columns
generated_states.columns = columns

costs["problem_size"] = all_problem_lengths
total_times["problem_size"] = all_problem_lengths
expanded_states["problem_size"] = all_problem_lengths
generated_states["problem_size"] = all_problem_lengths

# save all dataframes
costs.to_csv("3/data/costs.csv")
total_times.to_csv("3/data/total_times.csv")
expanded_states.to_csv("3/data/expanded_states.csv")
generated_states.to_csv("3/data/generated_states.csv")
