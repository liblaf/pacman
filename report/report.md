# Pacman Report

## Environment

- Python 3.9.7
- CPU: Intel(R) Core(TM) i7-10710U CPU @ 1.10GHz

## 问题一

### 测试结果

| Layout       | Function             | Heuristic             | Cost | Time (nanoseconds) | Search Nodes Expanded | Score |
| ------------ | -------------------- | --------------------- | ---- | ------------------ | --------------------- | ----- |
| `tinyMaze`   | `depthFirstSearch`   |                       | 8    | 429000             | 15                    | 502   |
| `tinyMaze`   | `breadthFirstSearch` |                       | 8    | 445100             | 15                    | 502   |
| `tinyMaze`   | `uniformCostSearch`  |                       | 8    | 354400             | 15                    | 502   |
| `tinyMaze`   | `aStarSearch`        | `nullHeuristic`       | 8    | 359100             | 15                    | 502   |
| `tinyMaze`   | `aStarSearch`        | `euclideanHeuristic`  | 8    | 359100             | 13                    | 502   |
| `tinyMaze`   | `aStarSearch`        | `manhattan_heuristic` | 8    | 426300             | 14                    | 502   |
| `mediumMaze` | `depthFirstSearch`   |                       | 246  | 8803000            | 269                   | 264   |
| `mediumMaze` | `breadthFirstSearch` |                       | 68   | 7522900            | 269                   | 442   |
| `mediumMaze` | `uniformCostSearch`  |                       | 68   | 8381000            | 269                   | 442   |
| `mediumMaze` | `aStarSearch`        | `nullHeuristic`       | 68   | 7891900            | 269                   | 442   |
| `mediumMaze` | `aStarSearch`        | `euclideanHeuristic`  | 68   | 9565000            | 226                   | 442   |
| `mediumMaze` | `aStarSearch`        | `manhattan_heuristic` | 68   | 6666400            | 221                   | 442   |
| `bigMaze`    | `depthFirstSearch`   |                       | 210  | 19604000           | 466                   | 300   |
| `bigMaze`    | `breadthFirstSearch` |                       | 210  | 26038300           | 620                   | 300   |
| `bigMaze`    | `uniformCostSearch`  |                       | 210  | 26098500           | 620                   | 300   |
| `bigMaze`    | `aStarSearch`        | `nullHeuristic`       | 210  | 30120300           | 620                   | 300   |
| `bigMaze`    | `aStarSearch`        | `euclideanHeuristic`  | 210  | 31310500           | 557                   | 300   |
| `bigMaze`    | `aStarSearch`        | `manhattan_heuristic` | 210  | 15353200           | 549                   | 300   |

### 分析

1. 在迷宫规模较小的情况下, 四种搜索方法的区别不大
2. 随着迷宫规模的扩大, 简单的 DFS 不能保证搜索到最优解, 但搜索到解的效率较高
3. BFS, UCS 及 A* 能够搜索到最优解
4. 在这一问中, BFS 与 UCS 是等价的, 其性能表现也基本一致
5. 有效的启发函数能够减小 A* 的开销

### Heuristic

使用 Manhattan Distance 作为 Heuristic.

#### Admissible

在没有墙的情况下, Pacman 到达 Goal 的最短路径长度即为 Manhattan Distance. 但在有墙的情况下, 真实的最短路径长度将不会小于 Manhattan Distance. 因此该 Heuristic 是 Admissible 的.

#### Consistency

$$
\begin{split}
h(n) - h(n')
& = |n.x - goal.x| + |n.y - goal.y| - |n'.x - goal.x| - |n'.y - goal.y| \\
& \leqslant |n.x - n'.x| + |n.y - n'.y| \\
& \leqslant ManhattanDistance(n, n') \\
& \leqslant c(n, a, n')
\end{split}
$$

因此该 Heuristic 满足 Consistency.

## 问题二

### 测试结果

| Layout            | Pacman            | Cost              | Time (nanoseconds) | Search Nodes Expanded | Score |
| ----------------- | ----------------- | ----------------- | ------------------ | --------------------- | ----- |
| `mediumScaryMaze` | `yourSearchAgent` | 8228.524537382846 | 17531600           | 177                   | 418   |
| `foodSearchMaze`  | `yourSearchAgent` | 36.0              | 8628100            | 15                    | 594   |

### `CostFn`

为了远离 Ghost, 我们令距离 Ghost 越近的位置代价越高. 为此, 首先以各个 Ghost 为起点进行一遍 BFS. 选取距离各个 Ghost 距离的倒数之和作为代价. 为了尽可能地远离 Ghost, 我们在此基础上再乘上一个较大的数, 例如 `wall_map.width * wall_map.height`, 以强调其相对于权重为 1 普通道路的重要性.

### 路径规划

将 Food 视为结点, 则问题转化为求最短哈密顿道路问题. 考虑到求解最优解的开销过大, 选择使用贪心的方法, 即从起点出发到达最近的 Food, 再到达下一个最近的 Food, 直至吃到所有 Food.

### 实现细节

因为只能修改 `SearchAgent` 的 `__init__` 函数, 所以不得已使用了一些丑陋的方法 hack 得到 `game_state`. 重写 `SearchProblem` 并将 `game_state` 保存在 `problem` 中. 在 `SearchProblem` 初始化时基于地图计算 `CostFn`. 基于 `uniformCostSearch` 编写适用于多个 Food 情况的 `SearchFunction`, 通过多次贪心地调用 `uniformCostSearch` 得到最短哈密顿道路的较优解.

## 问题三

### 设计迷宫

迷宫见 [google.lay](layouts/google.lay).

### 测试结果

录屏见 [problem-3.mp4](assets/problem-3.mp4).

| Layout           | Pacman           | Evaluation Function       | Depth | Total Time (nanoseconds) | Total Search Nodes Expaneded | Score |
| ---------------- | ---------------- | ------------------------- | ----- | ------------------------ | ---------------------------- | ----- |
| `trappedClassic` | `MinimaxAgent`   | `scoreEvaluationFunction` | 64    | 49119200                 | 926                          | -502  |
| `google`         | `MinimaxAgent`   | `eval_fn`                 | 1     | 23000094500              | 22071                        | 3718  |
| `trappedClassic` | `AlphaBetaAgent` | `scoreEvaluationFunction` | 64    | 5891700                  | 110                          | -502  |
| `google`         | `AlphaBetaAgent` | `eval_fn`                 | 1     | 22352491200              | 22071                        | 3718  |

### Agent: 摆!

在 `trappedClassic` 迷宫中, 吃豆人会首先冲向离它最近的怪物. 这是因为 `MinimaxAgent` 得出必死的结论, 所以会快速自杀以取得最小的时间惩罚.

### Alpha-Beta 剪枝

对比两 `Agent` 在 `trappedClassic` 中的表现, 不难发现 `AlphaBetaAgent` 的 "Total Search Nodes Expanded" 远小于 `MinimaxAgent`, 可见 Alpha-Beta 剪枝效果拔群. 但是在 `google` 中的表现却完全一致, 这可能是因为测试 `google` 时选取的搜索深度较浅, 决策强依赖于 Evaluation Function.

### Evaluation Function

#### v0

使用朴素的 `scoreEvaluationFunction`. 这样的弊端是 Evaluation Function 存在广阔的 "平原", 导致搜索不完全的情况下容易出现卡死.

#### v1

为了使 Pacman 不断靠近 Food, 我们在 `scoreEvaluationFunction` 的基础上增加一项估值, 即减去 Pacman 距离所有 Food Manhattan Distance 的和. 这样 Pacman 距离 Food 越远, 估值越低. 但是, 倘若地形复杂, Manhattan Distance 可能无法表征距离 Food 的真实路径长度, 导致被墙卡死.

#### v2

为了使 Pacman 能够真正靠近 Food, 我们在 v1 的基础上将距离修改为 BFS 得到的最短路. 然而, 在多个食物的情况下, 该估值函数仍然可能存在较大平原, 导致卡死.

#### v3

Food 虽好, 可不能贪多. 因此, 我们使用 `scoreEvaluationFunction` 减去离 Pacman 最近的 Food 的最短路径长度 `dist_to_closest_food` (由 BFS 得到) 作为估值. 这样确保 Pacman 目标坚定地朝向一个 Food, 而不会在多个 Food 之间摇摆不定. 但是, 这样做的问题在于. 在靠近一个 Food 后, 若剩下的 Food 都非常遥远, 那么吃掉这个 Food 将导致估值的下降 (尽管吃掉 Food 能够增加分数, 但最近的 Food 距离变得很遥远). 这将导致 Pacman 驻足在一个 Food 前 "不忍下口".

#### v4

为了让 Pacman 吃下眼前的 Food, 我们将吃掉一个 Food 的奖励调到足够高. 简单的做法就是: 将 `scoreEvaluationFunction` 一项乘上一个很大的数 (例如地图的面积 `map_area`) 就可以了.

#### v5

除了 Food 外, 还需要考虑 Ghost. 为了远离 Ghost, 我们在 v4 的基础上再添加一项: 距离所有 Ghost 距离的和. 这样, 距离 Ghost 越远, 估值越高. 但这样的问题在于, 吃掉 Capsule 将使得 Ghost 进入 Scared 状态, 不再构成威胁. 这导致该项突然减为 0. 于是会出现 Pacman "不忍" 吃掉 Capsule 的情况.

#### v6

我们调整一下与 Ghost 的距离这一项所占的比重, 采用平均值 `mean_dist_to_active_ghosts`, 同时调高与 Food 的距离 `dist_to_closest_food` 在总估值中的权重. 得到估值:

```python
state.getScore() * map_area - 2 * dist_to_closest_food + mean_dist_to_active_ghosts
```

#### v7

考虑到 Capsule 的存在, Pacman 并不必害怕 Scared Ghost, 相反 Pacman 应当适时主动出击. 因此, 我们再加入一项距离最近 Capsule 的距离和距离最近的 Scared Ghost 的距离 `dist_to_closest_scared_ghost`, 引导 Pacman 吃到 Capsule 并主动出击. 然而, Pacman 在面对 Capsule 的时候可能出现 v3 中描述的 "不忍下口" 的情况.

#### v8

仔细思考, 我们其实并不必显示地引导 Pacman 去吃 Capsule. ~~因为 Capsule 没分.~~ 因为吃下 Capsule 后, `dist_to_closest_scared_ghost` 将因此增大 (没有 Scared Ghost 时将其设为 `map_area`). 这样, 进一步调整各项权重, 我们得到了最终的估值函数:

```python
state.getScore() * map_area
- 2 * dist_to_closest_food
+ mean_dist_to_active_ghosts
- 4 * dist_to_closest_scared_ghost
```

