import pancake_problem

from pancake_problem import PancakeProblem
from queue import PriorityQueue
from search import Search, SearchNode

class HeuristicSearchNode(SearchNode):
    def __init__(self, state, parent, g, h, f):
        super().__init__(state, parent, g)
        self.h = h
        self.f = f

    def __lt__(self, obj):
        return self.f < obj.f

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
    start_node = HeuristicSearchNode(p.initial_state, None, 0, p.h(p.initial_state), p.h(p.initial_state))
    frontier.put(start_node) #g(s)
    self.generated += 1
    open_nodes = {} #set of candidates for expansion
    closed_nodes = {} #set of candidates removed from open because have smallest f(s)=g(s)+h(s)
    open_nodes[p.initial_state] = start_node
    closed_nodes[p.initial_state] = 0
    
    while not frontier.empty():
      node = frontier.get() #remove node with smallest f(s)=g(s)+h(s)
      self.expanded += 1
      closed_nodes[node.state] = node #add value of node into closed

      #for every successor s' of s such that s' is not in closed
      for action in p.actions(node.state):
        succ, cost = p.result(node.state, action)
        new_g = node.g + cost
        new_h = p.h(succ)*self.w
        new_f = new_g + new_h
        succ_node = HeuristicSearchNode(succ, node, new_g, new_h, new_f)
        if succ in open_nodes:
          open_nodes.pop(succ)
        elif succ in closed_nodes:
          # if cost <= new_g:
          #   continue
          #remove node from closed and open
          closed_nodes.pop(succ)
          
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

if __name__ == "__main__":
  problem = pancake_problem.generate_random_problem(5)
  problem = PancakeProblem((1, 5, 6, 2, 4, 3))
  problem.dump()
  astar = WeightedAStarSearch(problem, 1, print_statistics=True)
  astar.run()



