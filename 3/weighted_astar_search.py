from typing import Dict, Optional
import pancake_problem

from pancake_problem import PancakeProblem
from queue import PriorityQueue
from search import Search, SearchNode


class WeightedAStarSearch(Search):
  name = "weighted-astar"

  def __init__(self, search_problem, weight, **kwargs):
    super().__init__(search_problem, **kwargs)
    self.w = weight
    if weight == 0:
      self.name = "uniform-cost"
    elif weight == 1:
      self.name = "astar"

  def search(self):
    # early goal test for initial state
    p = self.search_problem
    if p.is_goal(p.initial_state):
      return [p.initial_state], 0

    # enqueue initial state
    frontier = PriorityQueue()
    frontier.put(SearchNode(p.initial_state, None, 0))
    self.generated += 1
    reached = {p.initial_state}

    while not frontier.empty():
      node = frontier.get()
      self.expanded += 1

      for action in p.actions(node.state):
        succ, cost = p.result(node.state, action)
        new_g = node.g + cost
        succ_node = SearchNode(succ, node, new_g)

        # early goal test
        if p.is_goal(succ):
          return self.extract_path(succ_node), new_g

        # mark reached to avoid cycles
        if succ not in reached:
          reached.add(succ)

          # enqueue successor
          frontier.put(succ_node)
          self.generated += 1

        if self.generated == self.max_generations:
          print("Aborting search after generating " +
            f"{self.max_generations} states without finding a solution.")
          return None, None

    # no solution found
    print("Explored entire search problem, no solution exists.")
    return None, None

"""
    #first own try on the solution

    # early goal test for initial state
    p = self.search_problem
    if p.is_goal(p.initial_state):
      return [p.initial_state], 0

    # enqueue initial state
    frontier = PriorityQueue()
    frontier.put(SearchNode(p.initial_state, None, 0)) #g(s)
    self.generated += 1
    open = {} #set of candidates for expansion
    closed = {} #set of candidates removed from open because have smallest f(s)=g(s)+h(s)
    open[p.initial_state] = None
    closed[p.initial_state] = 0
    
    while not frontier.empty():
      node = frontier.get() #remove node with smallest f(s)=g(s)+h(s)
      closed[p.initial_state] = node #add value of node into closed

      #for every successor s' of s such that s' is not in closed
      for action in p.actions(node.state):
        succ, cost = p.result(node.state, action)
        new_g = node.g + cost
        succ_node = SearchNode(succ, node, new_g)
        if succ in open and succ in closed:
          if cost <= new_g:
            continue
          #remove node from closed and open
          closed.pop(succ)
          open.pop(succ)
        #early goal testing  
        if p.is_goal(succ):
          return self.extract_path(succ_node), new_g
        #enqueue successor
        frontier.put(succ_node)
        self.generated += 1

        if self.generated == self.max_generations:
          print("Aborting search after generating " +
            f"{self.max_generations} states without finding a solution.")
          return None, None

    # no solution found
    print("Explored entire search problem, no solution exists.")
    return None, None  
"""      

if __name__ == "__main__":
  problem = pancake_problem.generate_random_problem(5)
  problem = PancakeProblem((1, 5, 6, 2, 4, 3))
  problem.dump()
  astar = WeightedAStarSearch(problem, 1, print_statistics=True)
  astar.run()



