# Name of group members:
#     Laurin van den Bergh
#     Nora Beringer
#     Yufeng Xiao

import search_problem

from queue import Queue
from search import Search, SearchNode


class UniformCostSearch(Search):
  name = "uniform-cost"

  def search(self):
    p = self.search_problem
    if p.is_goal(p.initial_state):
          return [p.initial_state], 0
    
    frontier = Queue()
    frontier.put(SearchNode(p.initial_state, None, 0))
    self.generated += 1
    reached = {p.initial_state}

    while not frontier.empty():
        node = frontier.get()
        self.expanded += 1

        reached.add(node.state)
        cost_collection = []
        for action in p.actions(node.state):
            succ, cost = p.result(node.state, action)
            if succ in reached:
                continue
            reached.add(succ)
            self.generated += 1
            cost_collection.append([succ, cost])
        '''a copy of queue but we can sort it with cost, then add its element into queue
           then we have a priority queue
        ''' 
        cost_collection.sort(key=lambda list: list[1]) 
        if (len(cost_collection) == 0):
              continue;
        for item in cost_collection:
            new_g = node.g + item[1]
            succ_node = SearchNode(item[0], node, new_g)
            frontier.put(succ_node)
        priority = cost_collection[0][0]
        priority_node = SearchNode(priority, node, 0)

        if p.is_goal(priority):
            return self.extract_path(priority_node), new_g

    return None, None


if __name__ == "__main__":
  problem = search_problem.generate_random_problem(8, 2, 3, max_cost=10)
  problem.dump()

  ucs = UniformCostSearch(problem, True)
  ucs.run()


