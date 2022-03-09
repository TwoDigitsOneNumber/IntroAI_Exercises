import search_problem

from search import Search, SearchNode


class UniformCostSearch(Search):
  name = "uniform-cost"

  def search(self):
    p = self.search_problem
    if p.is_goal(p.initial_state):
    	return [p.initial_state], 0
    
    #enque initial state
    frontier = [SearchNode(p.initial_state, None, 0)]
    self_generated += 1
    reached = {p.initial_state}
    
    seen = {}
    
    #while queue is not empty
    while not frontier.empty():
    	#pop node from queue
    	node = frontier.pop()
    	self.expanded += 1
    	
    	#mark seen objects
    	seen.add(node.state)
    	
    	#if seen and has lower cost
    	for action in p.actions(node.state):
        succ, cost = p.result(node.state, action)
        if succ in seen:
          continue
    	
    	#update the path
    	new_g = node.g + cost
        succ_node = SearchNode(succ, node, new_g)
        
        # early goal test
        if p.is_goal(succ):
          return self.extract_path(succ_node), new_g
    
    	# enqueue successor > this doen't work yet, how can we add another node while evaluating the cost
        for item in frontier(succ_node):
		item_cost = 1 if i == p.is_goal else 0
        	if item not in seen:
        		frontier.append(succ_node)
        		self.generated +=1
        		
  #No solution found 
  return None, None


if __name__ == "__main__":
  problem = search_problem.generate_random_problem(8, 2, 3, max_cost=10)
  problem.dump()
  ucs = UniformCostSearch(problem, True)
  ucs.run()


