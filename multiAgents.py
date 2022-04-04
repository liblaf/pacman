from game import Directions
import random, util

from game import Agent

#######################################################
#            This portion is written for you          #
#######################################################


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn="scoreEvaluationFunction", depth="2"):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################


import math
import time
import numpy as np
import game
import pacman


def shortest_distance(wall_map: game.Grid, pos: tuple[int, int]) -> np.ndarray:
    res = np.full(shape=(wall_map.width, wall_map.height), fill_value=np.inf)
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


def eval_fn(state: pacman.GameState):
    wall_map: game.Grid = state.getWalls()
    map_area = wall_map.width * wall_map.height
    shortest_dist = shortest_distance(wall_map=wall_map, pos=state.getPacmanPosition())
    dist_to_closest_food = min(
        [shortest_dist[food_x][food_y] for food_x, food_y in state.getFood().asList()],
        default=0,
    )
    scared_ghost_states: list[game.AgentState] = list(
        filter(lambda ghost_state: ghost_state.scaredTimer, state.getGhostStates())
    )
    scared_ghost_positions = [
        ghost_state.getPosition() for ghost_state in scared_ghost_states
    ]
    dist_to_scared_ghosts = [
        shortest_dist[int(ghost_x + 0.5)][int(ghost_y + 0.5)]
        for ghost_x, ghost_y in scared_ghost_positions
    ]
    dist_to_closest_scared_ghost = min(dist_to_scared_ghosts, default=map_area)
    active_ghost_states: list[game.AgentState] = list(
        filter(lambda ghost_state: not ghost_state.scaredTimer, state.getGhostStates())
    )
    active_ghost_positions = [
        ghost_state.getPosition() for ghost_state in active_ghost_states
    ]
    dist_to_active_ghosts = [
        shortest_dist[int(ghost_x + 0.5)][int(ghost_y + 0.5)]
        for ghost_x, ghost_y in active_ghost_positions
    ]
    mean_dist_to_active_ghosts = (
        sum(dist_to_active_ghosts, start=0) / len(active_ghost_positions)
        if active_ghost_states
        else map_area
    )

    return (
        state.getScore() * map_area
        - 2 * dist_to_closest_food
        + mean_dist_to_active_ghosts
        - 4 * dist_to_closest_scared_ghost
    )


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 3)
    """

    tot_cnt: int = 0
    tot_time_ns: int = 0

    def getAction(self, gameState: pacman.GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        we assume ghosts act in turn after the pacman takes an action
        so your minimax tree will have multiple min layers (one for each ghost)
        for every max layer

        gameState.generateChild(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state

        self.evaluationFunction(state)
        Returns pacman SCORE in current state (useful to evaluate leaf nodes)

        self.depth
        limits your minimax tree depth (note that depth increases one means
        the pacman and all ghosts has already decide their actions)
        """
        self.cnt: int = 0

        def minimax_value(
            state: pacman.GameState, agent_index: int = 0, depth: int = np.inf
        ):
            self.cnt += 1
            if (depth == 0) or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            next_agent_index = agent_index + 1
            next_depth = depth
            if next_agent_index == state.getNumAgents():
                next_agent_index = 0
                next_depth -= 1
            values = [
                minimax_value(
                    state=state.generateChild(agentIndex=agent_index, action=action),
                    agent_index=next_agent_index,
                    depth=next_depth,
                )
                for action in state.getLegalActions(agentIndex=agent_index)
            ]
            return (
                max(values, default=-np.inf)
                if agent_index == 0
                else min(values, default=np.inf)
            )

        start_time = time.perf_counter_ns()
        action = max(
            gameState.getLegalPacmanActions(),
            key=lambda action: minimax_value(
                state=gameState.generatePacmanChild(action=action),
                agent_index=1 % gameState.getNumAgents(),
                depth=self.depth,
            ),
        )
        end_time = time.perf_counter_ns()
        self.tot_cnt += self.cnt
        self.tot_time_ns += end_time - start_time
        print(
            f"Searched {self.cnt} states in {end_time - start_time} ns, Total {self.tot_cnt} states in {self.tot_time_ns} ns"
        )
        return action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    tot_cnt: int = 0
    tot_time_ns: int = 0

    def getAction(self, gameState: pacman.GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        self.cnt: int = 0

        def minimax_value(
            state: pacman.GameState,
            agent_index: int = 0,
            alpha: float = -np.inf,
            beta: float = np.inf,
            depth: int = np.inf,
        ):
            self.cnt += 1
            if (depth == 0) or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            next_agent_index = agent_index + 1
            next_depth = depth
            if next_agent_index == state.getNumAgents():
                next_agent_index = 0
                next_depth -= 1
            next_states = [
                state.generateChild(agentIndex=agent_index, action=action)
                for action in state.getLegalActions(agentIndex=agent_index)
            ]
            if agent_index == 0:  # pacman, max-node
                value = -np.inf
                for next_state in next_states:
                    value = max(
                        value,
                        minimax_value(
                            state=next_state,
                            agent_index=next_agent_index,
                            alpha=alpha,
                            beta=beta,
                            depth=next_depth,
                        ),
                    )
                    if value >= beta:
                        return value
                    alpha = max(alpha, value)
            else:  # ghost, min-node
                value = np.inf
                for next_state in next_states:
                    value = min(
                        value,
                        minimax_value(
                            state=next_state,
                            agent_index=next_agent_index,
                            alpha=alpha,
                            beta=beta,
                            depth=next_depth,
                        ),
                    )
                    if value <= alpha:
                        return value
                    beta = min(beta, value)
            return value

        start_time = time.perf_counter_ns()
        action = max(
            gameState.getLegalPacmanActions(),
            key=lambda action: minimax_value(
                state=gameState.generatePacmanChild(action=action),
                agent_index=1 % gameState.getNumAgents(),
                depth=self.depth,
            ),
        )
        end_time = time.perf_counter_ns()
        self.tot_cnt += self.cnt
        self.tot_time_ns += end_time - start_time
        print(
            f"{self.cnt} search nodes expanded in {end_time - start_time} ns, Totally {self.tot_cnt} search nodes expanded in {self.tot_time_ns} ns"
        )
        return action
