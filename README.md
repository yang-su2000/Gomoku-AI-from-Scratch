Gomoku AI from scratch
======================

Showcase:
---------
- https://youtu.be/5QnG0_ijQdA
<img src="images/Gomoku-Demo.gif" width=600 height=600>

Play:
-----
- install pygame: `pip install pygame`
- For player:
  - run `python play.py`
- For developer:
  - run `python main.py`
  - To play against AI 0.0, set depth = -1
  - To play against AI 1.0, set depth = 0
  - To play against AI 2.0, set depth > 0 and width > 0
- on Mac, it is known that the font we use is not default
  - we locate the font from "C:\Windows\Fonts\Candarab.ttf" on windows, try to install on Mac accordingly

Intro:
------
- Hi! this is a project named "Tackle the Game of Gomoku by using Minimax with Multilayer Heuristics".

- The Algorithm mainly redesigns the traditional Minimax with alpha-beta pruning used for Gomoku by utilizing multi-layer heuristics in the neural network and the discounted factor in reinforcement learning. Experiment results show that the algorithm can beat amateur human players in most cases with only several seconds of thinking time in each round at its shallowest depth.

Abstract:
---------
- Gomoku, also called five-in-a-row, is a popular abstract strategy board game developed by humans in the 19th century. Classical methods to tackle the game by purely tree-based Minimax algorithm do not achieve good results because of its limitation in both search depth and width. In this project, I try to assign heuristics from the surroundings of each possibly winnable grid and build a multi-layer threat space searching algorithm on top of that. Earlier layers perform mainly for restriction and enforcement in sensing the threat and later ones utilize trainable ranks for pruning the search space.

- Experiment results show that this approach outperforms traditional Minimax from closest neighborhood searching and generates interesting outcomes against amateur human players. The algorithm parameters are constructed in a neural-network-like and self-correlated way, and it can be easily adopted by reinforcement learning methods like Monte Carlo Tree Search. This algorithm serves as a new approach of including multi-layer heuristics in RL for board game AI.

Feature:
--------
- No external library other than pygame for UI display
- AI 0.0: one step with rank
- AI 0.5: one step with score (discarded)
- AI 1.0: one step with rank + score
- AI 2.0: max (depth, width) steps (6, 5) or (10, 2) or (4, All board) supported minimax with rank

Issues:
-------
- version 2.3
  - AI assumes player to be as rational as itself, which leads to flaws in move predictions

Debug:
------
- computer debug is in method "final_move"
- main debug is changed by setting if condition 0/1 AND comment in/out the "game.quit()" in `game.py`

Record:
------
- Black : White : Draw
- v1.5: 
  - AI 0.0 vs. AI 0.0 1000 runs, 526 : 413 : 43
- v1.9:
  - AI 0.0 vs. AI 0.0 100 runs, 45 : 39 : 16
  - AI 1.0 vs. AI 1.0 100 runs, 48 : 34 : 18
  - AI 1.0 vs. AI 0.0 200 runs, 86 : 57 : 67
  - AI 0.0 vs. AI 1.0 200 runs, 45 : 69 : 86
- v2.2: (depth = 4, width = 3)
  - AI 2.0 vs. AI 2.0 100 runs, 55 : 38 : 7
  - AI 2.0 vs. AI 1.0 100 runs, 53 : 33 : 14
  - AI 1.0 vs. AI 2.0 100 runs, 43 : 46 : 11
  - AI 2.0 vs. AI 0.0 100 runs, 45 : 29 : 26
  - AI 0.0 vs. AI 2.0 100 runs, 32 : 44 : 24

Game Rule:
----------
- Q: Quit Game
- Change main.py to set AI / human, set Black / White, and set delay (for AI vs. AI only)

Stable Version:
---------------
- v1.5: One step heuristic
- v1.6: (depth, width) = (1, 1) converges to v1.5 deterministic version
- v1.9: One step with rank, when (depth, width) != (1, 1) AI plays with low randomness
- v2.2: Minimax step with rank, defensive attack implemented

Other:
------
- UI is inspired by https://blog.csdn.net/weixin_42756970/article/details/106493570 and https://github.com/sepandhaghighi/art
