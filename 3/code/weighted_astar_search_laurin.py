from re import S
import pancake_problem

from pancake_problem import PancakeProblem
from queue import PriorityQueue
from search import Search, SearchNode

class ComparableSearchNode(SearchNode):
  def __lt__(self, other):
    return self.state < other.state


class WeightedAStarSearch(Search):
  name = "weighted-astar"

  def __init__(self, search_problem, weight, **kwargs):
    super().__init__(search_problem, **kwargs)
    self.w = weight
    if weight == 0:
      self.name = "uniform-cost"
    elif weight == 1:
      self.name = "astar"
    else:
      self.name = f"weighted_astar_{weight}"

  def f(self, state, g):
    return g + self.search_problem.h(state)


  def search(self):
    # early goal test for initial state
    p = self.search_problem
    if p.is_goal(p.initial_state):
      return [p.initial_state], 0

    # implement A* search

    # initialize frontier with initial state (elements are tuples like: (f_of_node, node))
    frontier = PriorityQueue()
    f_of_initial_state = 0 + self.w * p.h(p.initial_state)
    frontier.put( (f_of_initial_state, ComparableSearchNode(p.initial_state, None, 0)) )

    # initialize reached set as dictionary (key: state, value: node), and add initial state
    reached = {p.initial_state: SearchNode(p.initial_state, None, 0)}

    # iterate over frontier
    while not frontier.empty():
      f_node, node = frontier.get()

      # if goal is found, return the node associated with the goal state
      if p.is_goal(node.state):
        return self.extract_path(node), node.g # return solution (path from initial state to goal state) and cost of the solution

      # iterate over all actions
      for a in p.actions(node.state):
        s_prime, cost_of_a = p.result(node.state, a)
        c = node.g + cost_of_a

        # reopening if necessary
        if (not s_prime in reached) or (c < reached[s_prime].g):
          child = ComparableSearchNode(s_prime, node, c)
          reached[s_prime] = child
          f_of_child = child.g + self.w * p.h(child.state)
          frontier.put( (f_of_child, child) )
    
    # if this part of the code is reached, then no solution was found, i.e. no solution exists
    print("Explored entire search problem, no solution exists.")
    return None, None

      





    return plan, cost
    # raise NotImplementedError

if __name__ == "__main__":
  problem = pancake_problem.generate_random_problem(5)
  problem = PancakeProblem((1, 5, 6, 2, 4, 3))
  problem.dump()
  astar = WeightedAStarSearch(problem, 1, print_statistics=True)
  astar.run()



