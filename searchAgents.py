"""
This file contains all of the agents that can be selected to control Pacman.  To
select an agent, use the '-p' option when running pacman.py.  Arguments can be
passed to your agent using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a fn=depthFirstSearch

Commands to invoke other search strategies can be found in the project
description.

Please only change the parts of the file you are asked to.  Look for the lines
that say

"*** YOUR CODE HERE ***"

The parts you fill in start about 3/4 of the way down.  Follow the project
description for details.

Good luck and happy searching!
"""

from game import Directions
from game import Agent
from game import Actions
import util
import time
import search

#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py          #
#######################################################


class GoWestAgent(Agent):
    "An agent that goes West until it can't."

    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        if Directions.WEST in state.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP


class SearchAgent(Agent):
    """
    This very general search agent finds a path using a supplied search
    algorithm for a supplied search problem, then returns actions to follow that
    path.

    As a default, this agent runs DFS on a PositionSearchProblem to find
    location (1,1)

    Options for fn include:
      depthFirstSearch
      breadthFirstSearch
      uniformCostSearch
      aStarSearch

    Note: You should NOT change any code in SearchAgent
    """

    def __init__(
        self,
        fn="depthFirstSearch",
        prob="PositionSearchProblem",
        heuristic="nullHeuristic",
    ):
        # Warning: some advanced Python magic is employed below to find the right functions and problems

        # Get the search function from the name and heuristic
        if fn not in dir(search):
            raise AttributeError(fn + " is not a search function in search.py.")
        func = getattr(search, fn)
        if "heuristic" not in func.__code__.co_varnames:
            print("[SearchAgent] using function " + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
            else:
                raise AttributeError(
                    heuristic + " is not a function in searchAgents.py or search.py."
                )
            print("[SearchAgent] using function %s and heuristic %s" % (fn, heuristic))
            # Note: this bit of Python trickery combines the search algorithm and the heuristic
            self.searchFunction = lambda x: func(x, heuristic=heur)

        # Get the search problem type from the name
        if prob not in globals().keys() or not prob.endswith("Problem"):
            raise AttributeError(
                prob + " is not a search problem type in SearchAgents.py."
            )
        self.searchType = globals()[prob]
        print("[SearchAgent] using problem type " + prob)

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game
        board. Here, we choose a path to the goal. In this phase, the agent
        should compute the path to the goal and store it in a local variable.
        All of the work is done in this method!

        state: a GameState object (pacman.py)
        """
        if self.searchFunction == None:
            raise Exception("No search function provided for SearchAgent")
        starttime = (
            time.perf_counter_ns()
        )  # You can use also time.perf_counter_ns() for more pecision
        problem = self.searchType(state)  # Makes a new search problem
        self.actions = self.searchFunction(problem)  # Find a path
        totalCost = problem.getCostOfActionSequence(self.actions)
        print(
            f"Path found with total cost of {totalCost} in {time.perf_counter_ns() - starttime} nanoseconds"
        )
        if "_expanded" in dir(problem):
            print("Search nodes expanded: %d" % problem._expanded)

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in
        registerInitialState).  Return Directions.STOP if there is no further
        action to take.

        state: a GameState object (pacman.py)
        """
        if "actionIndex" not in dir(self):
            self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP


class PositionSearchProblem(search.SearchProblem):
    """
    A search problem defines the state space, start state, goal test, child
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(
        self,
        gameState,
        costFn=lambda x: 1,
        goal=(1, 1),
        start=None,
        warn=True,
        visualize=True,
    ):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None:
            self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print("Warning: this does not look like a regular search maze")

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0  # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__

            if "_display" in dir(__main__):
                if "drawExpandedCells" in dir(__main__._display):  # @UndefinedVariable
                    __main__._display.drawExpandedCells(
                        self._visitedlist
                    )  # @UndefinedVariable

        return isGoal

    def expand(self, state):
        """
        Returns child states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (child, action, stepCost), where 'child' is a
         child to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that child
        """

        children = []
        for action in self.getActions(state):
            nextState = self.getNextState(state, action)
            cost = self.getActionCost(state, action, nextState)
            children.append((nextState, action, cost))

        # Bookkeeping for display purposes
        self._expanded += 1  # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return children

    def getActions(self, state):
        possible_directions = [
            Directions.NORTH,
            Directions.SOUTH,
            Directions.EAST,
            Directions.WEST,
        ]
        valid_actions_from_state = []
        for action in possible_directions:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                valid_actions_from_state.append(action)
        return valid_actions_from_state

    def getActionCost(self, state, action, next_state):
        assert next_state == self.getNextState(
            state, action
        ), "Invalid next state passed to getActionCost()."
        return self.costFn(next_state)

    def getNextState(self, state, action):
        assert action in self.getActions(
            state
        ), "Invalid action passed to getActionCost()."
        x, y = state
        dx, dy = Actions.directionToVector(action)
        nextx, nexty = int(x + dx), int(y + dy)
        return (nextx, nexty)

    def getCostOfActionSequence(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions == None:
            return 999999
        x, y = self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += self.costFn((x, y))
        return cost


def euclideanHeuristic(position, problem, info={}):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5


class StayEastSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the West side of the board.

    The cost function for stepping into a position (x,y) is 1/2^x.
    """

    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: 0.5 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(
            state, costFn, (1, 1), None, False
        )


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################


import numpy as np
import game
import pacman
import search


def manhattan_heuristic(position, problem, info={}):
    "The heuristic distance for a PositionSearchProblem"
    return util.manhattanDistance(position, problem.goal)


class MySearchProblem(PositionSearchProblem):
    game_state: pacman.GameState = None
    food_map: game.Grid = None

    def __init__(
        self,
        gameState: pacman.GameState,
        costFn=lambda x: 1,
        goal: tuple = (1, 1),
        start: tuple = None,
        warn: bool = True,
        visualize: bool = True,
    ):
        super().__init__(gameState, costFn, goal, start, warn, visualize)

        def build_cost_fn(game_state: pacman.GameState):
            def shortest_distance(
                wall_map: game.Grid, pos: tuple[int, int]
            ) -> np.ndarray:
                res = np.full(
                    shape=(wall_map.width, wall_map.height), fill_value=np.inf
                )
                frontier = util.Queue()
                frontier.push(item=pos)
                x, y = pos
                res[x][y] = 0
                while not frontier.isEmpty():
                    current_x, current_y = frontier.pop()
                    for next_x, next_y in game.Actions.getLegalNeighbors(
                        position=(current_x, current_y), walls=wall_map
                    ):
                        if res[next_x][next_y] < np.inf:
                            continue
                        res[next_x][next_y] = res[current_x][current_y] + 1
                        frontier.push(item=(next_x, next_y))
                return res

            wall_map: game.Grid = game_state.getWalls()
            cost_map = np.ones(shape=(wall_map.width, wall_map.height))
            for ghost_x, ghost_y in game_state.getGhostPositions():
                cost_map += (
                    wall_map.width
                    * wall_map.height
                    / shortest_distance(wall_map=wall_map, pos=(ghost_x, ghost_y))
                )
            return lambda pos: cost_map[pos[0]][pos[1]]

        self.game_state = gameState
        self.food_map = gameState.getFood().deepCopy()
        self.costFn = build_cost_fn(game_state=gameState)

    def isGoalState(self, state: tuple) -> bool:
        return self.food_map[state[0]][state[1]]


class yourSearchAgent(SearchAgent):
    """
    You can design different SearchAgents for different Mazes
    """

    def __init__(self):
        super().__init__(prob="MySearchProblem")

        def MySearchFunction(problem: MySearchProblem):
            actions: list = []
            while problem.food_map.count():
                actions_to_next_food: list = search.uniformCostSearch(problem=problem)
                for action in actions_to_next_food:
                    problem.startState = problem.getNextState(
                        state=problem.startState, action=action
                    )
                actions += actions_to_next_food
                problem.food_map[problem.startState[0]][problem.startState[1]] = False
            problem.startState = problem.game_state.getPacmanPosition()
            return actions

        self.searchFunction = MySearchFunction
