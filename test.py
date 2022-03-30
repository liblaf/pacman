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
    heuristics = ["nullHeuristic", "euclideanHeuristic", "yourHeuristic"]
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


if __name__ == "__main__":
    argvs = []
    if (len(sys.argv) < 2) or (sys.argv[1] == "1"):
        argvs = prepare_problem_1()
    else:
        pass
    for argv in argvs:
        cmd = [
            "python",
            "pacman.py",
            "--quietTextGraphics",
            f"--layout={argv['layout']}",
            f"--pacman={argv['pacman']}",
        ]
        if "agentArgs" in argv:
            agentArgs = []
            for key, value in argv["agentArgs"].items():
                agentArgs.append(f"{key}={value}")
            agentArgs = ",".join(agentArgs)
            cmd.append(f"--agentArgs={agentArgs}")
        os.system(" ".join(cmd))
