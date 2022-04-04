import re
import os
import sys


def get_layouts(path: str = "./layouts/") -> list:
    layouts = []
    for filename in os.listdir(path=path):
        match = re.match(pattern="(\w*).lay", string=filename)
        if match:
            layouts.append(match.group(1))
    return layouts


def prepare_problem_1():
    layouts = ["tinyMaze", "mediumMaze", "bigMaze"]
    fns = ["depthFirstSearch", "breadthFirstSearch", "uniformCostSearch", "aStarSearch"]
    heuristics = ["nullHeuristic", "euclideanHeuristic", "manhattan_heuristic"]
    argvs = []
    for layout in layouts:
        for fn in fns:
            if fn == "aStarSearch":
                for heuristic in heuristics:
                    argvs.append(
                        {
                            "layout": layout,
                            "pacman": "SearchAgent",
                            "agentArgs": {"fn": fn, "heuristic": heuristic},
                        }
                    )
            else:
                argvs.append(
                    {"layout": layout, "pacman": "SearchAgent", "agentArgs": {"fn": fn}}
                )
    return argvs


def prepare_problem_2():
    argvs = [
        {"layout": "mediumScaryMaze", "pacman": "yourSearchAgent"},
        {"layout": "foodSearchMaze", "pacman": "yourSearchAgent"},
    ]
    return argvs


def prepare_problem_3():
    argvs = [
        {
            "layout": "trappedClassic",
            "pacman": "MinimaxAgent",
            "agentArgs": {"depth": 64},
            "frameTime": 1,
        },
        {
            "layout": "google",
            "pacman": "MinimaxAgent",
            "agentArgs": {"evalFn": "eval_fn", "depth": 1},
            "frameTime": 0,
        },
        {
            "layout": "trappedClassic",
            "pacman": "AlphaBetaAgent",
            "agentArgs": {"depth": 64},
            "frameTime": 1,
        },
        {
            "layout": "google",
            "pacman": "AlphaBetaAgent",
            "agentArgs": {"evalFn": "eval_fn", "depth": 1},
            "frameTime": 0,
        },
    ]
    return argvs


if __name__ == "__main__":
    argvs = []
    if (len(sys.argv) < 2) or (sys.argv[1] == "1"):
        argvs = prepare_problem_1()
    elif sys.argv[1] == "2":
        argvs = prepare_problem_2()
    elif sys.argv[1] == "3":
        argvs = prepare_problem_3()
        pass
    for argv in argvs:
        cmd = [
            "python",
            "pacman.py",
            f"--layout={argv['layout']}",
            f"--pacman={argv['pacman']}",
            "--quietTextGraphics",
            # "--zoom=1.0",
            "--fixRandomSeed",
        ]
        if "frameTime" in argv:
            cmd.append(f"--frameTime={argv['frameTime']}")
        if "agentArgs" in argv:
            agentArgs = []
            for key, value in argv["agentArgs"].items():
                agentArgs.append(f"{key}={value}")
            agentArgs = ",".join(agentArgs)
            cmd.append(f"--agentArgs={agentArgs}")
        print(" ".join(cmd))
        os.system(" ".join(cmd))
