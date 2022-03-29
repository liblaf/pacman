"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

#######################################################
#            This portion is written for you          #
#######################################################


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A example of heuristic function which estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial. You don't need to edit this function
    """
    return 0


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions

    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    """
    explored = {}

    def dfs(state=problem.getStartState(), actions: util.Stack = None) -> list:
        if state in explored:
            return []
        actions = actions or util.Stack()
        if problem.isGoalState(state):
            return actions.list
        explored[state] = True
        for next_state, action, action_cost in problem.expand(state):
            actions.push(action)
            next_actions = dfs(next_state, actions)
            if next_actions:
                return next_actions
            actions.pop()

    return dfs()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    explored = {}  # state -> actions
    frontier = util.Queue()
    frontier_data = {}  # state -> actions
    start_state = problem.getStartState()
    frontier.push(start_state)
    frontier_data[start_state] = []
    while not frontier.isEmpty():
        current_state = frontier.pop()
        current_actions = frontier_data[current_state]
        frontier_data.pop(current_state)
        if problem.isGoalState(current_state):
            return current_actions
        explored[current_state] = current_actions
        for next_state, action, action_cost in problem.expand(current_state):
            if not ((next_state in frontier_data) or (next_state in explored)):
                frontier.push(next_state)
                frontier_data[next_state] = current_actions + [action]
    return []


def uniformCostSearch(problem):
    """Search the node of least cost from the root."""
    explored = {}  # state -> actions, cost
    frontier = util.PriorityQueue()
    frontier_data = {}  # state -> actions, cost
    start_state = problem.getStartState()
    frontier.push(start_state, 0)
    frontier_data[start_state] = [], 0
    while not frontier.isEmpty():
        current_state = frontier.pop()
        current_actions, current_cost = frontier_data[current_state]
        frontier_data.pop(current_state)
        if problem.isGoalState(current_state):
            return current_actions
        explored[current_state] = current_actions, current_cost
        for next_state, action, action_cost in problem.expand(current_state):
            next_cost = current_cost + action_cost
            if not ((next_state in frontier_data) or (next_state in explored)):
                frontier.push(next_state, next_cost)
                frontier_data[next_state] = current_actions + [action], next_cost
            elif (next_state in frontier_data) and (
                frontier_data[next_state][1] > next_cost
            ):
                frontier.update(next_state, next_cost)
                frontier_data[next_state] = current_actions + [action], next_cost
    return []


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    explored = {}  # state -> actions, g
    frontier = util.PriorityQueue()
    frontier_data = {}  # state -> actions, g
    start_state = problem.getStartState()
    frontier.push(start_state, 0)
    frontier_data[start_state] = [], 0
    while not frontier.isEmpty():
        current_state = frontier.pop()
        current_actions, current_g = frontier_data[current_state]
        frontier_data.pop(current_state)
        if problem.isGoalState(current_state):
            return current_actions
        explored[current_state] = current_actions, current_g
        for next_state, action, action_cost in problem.expand(current_state):
            next_g = current_g + action_cost
            next_h = heuristic(next_state, problem)
            if not ((next_state in frontier_data) or (next_state in explored)):
                frontier.push(next_state, next_g + next_h)
                frontier_data[next_state] = current_actions + [action], next_g
            elif (next_state in frontier_data) and (
                frontier_data[next_state][1] > next_g
            ):
                frontier.update(next_state, next_g + next_h)
                frontier_data[next_state] = current_actions + [action], next_g
    return []
