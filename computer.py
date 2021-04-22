from board import *
from copy import deepcopy
import random

class Computer:
    def __init__(self, is_black, board, depth, width):

        self.color = 2 if is_black else 1 # constant
        self.opponent_color = 1 if is_black else 2
        self.board = board
        self.h_grid = [] # the heuristic board, should only be used and modified by computer
        self.dict_grid = []
        for i in range(self.board.piece_num):
            self.h_grid.append(list([(0, 0)] * self.board.piece_num))
            self.dict_grid.append(list([""] * self.board.piece_num))
        self.cal_count = None # debug for counting number of configurations we exhausted
        self.power_depth = depth
        self.power_width = width
        # self.final_pos = None
        # self.opponent_penalized_factor = 0.9
        """ 
        Final task:
        Update h_dictionary in genetic search to achieve [reinforcement learning], initial value denotes (rank, score)

        Ranking and Scoring:
        RANK 1 [strictly >] RANK 2 [strictly >] RANK 3 [strictly >] RANK 4 [?] RANK 5 [?] RANK 6 [strictly >] RANK 10

        High ranks mostly performs as a "enforcement", lower ranks more likely performs as pruning strategy to reduce time complexity
        High scores is just a temporary way to denote the "expected" preferred move by assigned heuristic values, but no gurantee on "actual" performance

        RANK -1: to denote filled cell
        RANK 0: to denote empty (non-intialized) cell
        RANK 1 "winning move": move that I win immediately
        RANK 2 "winning move": move that opponent wins immediately
        RANK 3 "next winning move": move that me / opponent must lose as a matter of time, if they do not have a "winning move"
        RANK 4 "aggressive move": move that forces me / opponent to place certain position to avoid losing, restricts the move position to a local range
        RANK 5 "mindful move": move that has a chance to be aggressive later on, but no guarantee
        RANK 6 "random move": move that ... does not look useful, maybe genetic search can make it useful?
        RANK 7 "dead move": move that is useless, dead inside
        RANK -100 / 100: used in minimax for assigning initial upper and lower bound
        """
        self.dict = {
            "my win 5": (1, 100000), # my only winning move
            "op win 5": (2, 90000), # op only winning move
            "my open 3+4": (3, 9000), "my open 3+3": (3, 4000), 
            "op open 3+4": (3, 6000), "op open 3+3": (4, 2000),
            "my open 4": (3, 10000), "op open 4": (3, 7000), # next winning move
            "my sep 5": (4, 500), "my sleep 4": (4, 500), "my open 3": (4, 350), "my sep 4": (4, 300), # aggressive move
            "op sep 5": (4, 450), "op sleep 4": (4, 400), "op open 3": (4, 250), "op sep 4": (4, 200),
            "my sep 3": (4, 20), "my open 2": (4, 50), "my sleep 3": (4, 30),
            "op sep 3": (4, 5), "op open 2": (4, 10), "op sleep 3": (4, 7),
            "my open 1": (6, 1), "my sleep 1": (6, 1), "my sleep 2": (6, 1), # random move
            "op open 1": (6, 0), "op sleep 2": (6, 0), "op sleep 1": (6, 0), 
            "my dead": (7, 0), # dead move
            "op dead": (7, 0),
            "wall": (7, -1), "wall 2": (7, -2),
            "alpha": (100, 1000000),
            "beta": (-100, -1000000)
            }
        self.my_dict = {
            "my win 5": (1, 100000), # my only winning move
            "op win 5": (2, 90000), # op only winning move
            "my open 3+4": (3, 9000), "my open 3+3": (3, 4000), 
            "op open 3+4": (3, 6000), "op open 3+3": (4, 2000),
            "my open 4": (3, 10000), "op open 4": (3, 7000), # next winning move
            "my sep 5": (4, 500), "my sleep 4": (4, 500), "my open 3": (4, 350), "my sep 4": (4, 300), # aggressive move
            "op sep 5": (4, 450), "op sleep 4": (4, 400), "op open 3": (4, 250), "op sep 4": (4, 200),
            "my sep 3": (4, 20), "my open 2": (4, 50), "my sleep 3": (4, 30),
            "op sep 3": (4, 5), "op open 2": (4, 10), "op sleep 3": (4, 7),
            "my open 1": (6, 1), "my sleep 1": (6, 1), "my sleep 2": (6, 1), # random move
            "op open 1": (6, 0), "op sleep 2": (6, 0), "op sleep 1": (6, 0), 
            "my dead": (7, 0), # dead move
            "op dead": (7, 0),
            "wall": (7, -1), "wall 2": (7, -2),
            "alpha": (100, 1000000),
            "beta": (-100, -1000000)
            }
        self.op_dict = {
            "op win 5": (1, 100000), # my only winning move
            "my win 5": (2, 90000), # op only winning move
            "op open 3+4": (3, 9000), "op open 3+3": (3, 4000), 
            "my open 3+4": (3, 6000), "my open 3+3": (4, 2000),
            "op open 4": (3, 10000), "my open 4": (3, 7000), # next winning move
            "op sep 5": (4, 500), "op sleep 4": (4, 500), "op open 3": (4, 350), "op sep 4": (4, 300), # aggressive move
            "my sep 5": (4, 450), "my sleep 4": (4, 400), "my open 3": (4, 250), "my sep 4": (4, 200),
            "op sep 3": (4, 20), "op open 2": (4, 50), "op sleep 3": (4, 30),
            "my sep 3": (4, 5), "my open 2": (4, 10), "my sleep 3": (4, 7),
            "op open 1": (6, 1), "op sleep 1": (6, 1), "op sleep 2": (6, 1), # random move
            "my open 1": (6, 0), "my sleep 2": (6, 0), "my sleep 1": (6, 0), 
            "op dead": (7, 0), # dead move
            "my dead": (7, 0),
            "wall": (7, -1), "wall 2": (7, -2),
            "alpha": (100, 1000000),
            "beta": (-100, -1000000)
            }
        for r in range(self.board.piece_num):
            for c in range(self.board.piece_num):
                self.update_heuristic(r, c)

    def final_move(self):
        
        if self.board.round == 0: # initial move at middle
            return (self.board.piece_num // 2 - 1, self.board.piece_num // 2 - 1)
        new_piece = self.get_opponent_piece() # the opponent just placed a new piece, what is it?
        # print("opponent at", new_piece[0], new_piece[1])
        self.notify_my_neighbor(new_piece[0], new_piece[1]) # tell my heuristic grid about this new piece

        ''' debug '''
        # self.print_h_board()
        # self.print_score_board()
        # self.print_rank_board()

        if self.is_draw():
            return (-10, -10)
        if self.power_depth == 0:
            return self.move_piece_1()
        elif self.power_depth == -1:
            return self.move_piece_0()
        else:
            return self.move_piece_2(self.power_depth, self.power_width, False) # search depth, search width, is_naive

    def get_opponent_piece(self):

        b = self.board
        for r in range(b.piece_num):
            for c in range(b.piece_num):
                if b.r_grid[r][c] == b.round: # the opponent placed this piece in the round just now
                    return (r, c)

    def notify_my_neighbor(self, r, c):

        b = self.board
        for i in range(max(r - 4, 0), min(r + 5, b.piece_num)): # update heuristic of each possible piece in the neighborhood
            for j in range(max(c - 4, 0), min(c + 5, b.piece_num)):
                self.update_heuristic(i, j)

    def is_higher_conf(self, a, b): # two configrations a, b = (rank, score), is a > b?
        return a[0] < b[0] or (a[0] == b[0] and a[1] > b[1])

    def is_draw(self):

        b = self.board
        for r in range(b.piece_num):
            for c in range(b.piece_num):
                if self.h_grid[r][c][0] > 0 and self.h_grid[r][c][0] < 6: # empty and winnable cell 
                    return False
        return True # no empty cell

    """
    AI 2.0: minimax (is_naive: compare with rank + score, fast version; !is_naive: compare with rank only, slow version)
    """
    def move_piece_2(self, depth, width, is_naive):

        b = self.board
        self.power_depth = depth
        # self.final_pos = None
        origin_grid = deepcopy(b.grid) # deepcopy the current board
        origin_h_grid = deepcopy(self.h_grid)
        eval_list = [None] * depth
        conf_list = [None] * depth
        pos_list = [None] * depth
        for i in range(0, depth):
            conf_list[i] = 'alpha' if (self.power_depth - i) % 2 else 'beta'
            eval_list[i] = self.dict['alpha'] if (self.power_depth - i) % 2 else self.dict['beta']
            pos_list[i] = set()
        initial_search_set = self.fetch_optimal_search_set(pos_list, conf_list, eval_list, depth - 1, width, is_naive)
        # if self.final_pos is not None:
        #     return self.final_pos

        self.cal_count = [0] * depth # debug
        self.minimax(initial_search_set, pos_list, conf_list, eval_list, depth - 1, width, is_naive)
        # if self.final_pos is not None:
        #     return self.final_pos
        for i in range(0, depth): # debug
            # print("fetched", self.cal_count[i], "configurations at depth", i)
            # print("pos =", end=" ")
            # for pos in pos_list[i]:
            #     print(pos, end=" ")
            # print("\n(rank, score) =", eval_list[i])
            pass

        b.grid = origin_grid # restore the board
        self.h_grid = origin_h_grid
        if b.debug_delay > 0: # restore the trace for visualization
            for r in range(b.piece_num):
                for c in range(b.piece_num):
                    b.trace_grid[r][c] = 5

        # fetch the optimal position on maximum depth
        maxConf = self.dict['alpha']
        posList = []
        for (r, c) in pos_list[depth - 1]:
            conf = self.h_grid[r][c]
            if self.is_higher_conf(conf, maxConf):
                maxConf = conf
                # print("new maxConf:", maxConf[0], maxConf[1])
                posList.clear()
                posList.append((r, c))
            elif conf == maxConf:
                posList.append((r, c))

        """
        Improve this randomness by searching deeper or wider
        """
        rand_choice = random.randint(0, len(posList) - 1) # randomly choose one "optimal" move
        pos = posList[rand_choice]
        # print("the optimal list length is", len(posList), "the choice is", rand_choice)
        # print("the final position is", pos[0], pos[1], "with rank =", maxConf[0], "score =", maxConf[1])

        return pos

    # pos_list: a list containing my max pos for each depth
    # conf_list: a list containing my max configuration for each depth, sync with eval_list
    # eval_list: a list containing my max configuration value for each depth
    # is_naive: if true, generating configurations with same rank and score, else generating configurations with same rank
    def minimax(self, search_set, pos_list, conf_list, eval_list, depth, width, is_naive):

        # if self.final_pos is not None:
        #     return

        self.cal_count[depth] += len(search_set) # debug

        if depth == 0:
            for pos in search_set: # append all optimal positions to pos_list and done
                pos_list[depth].add(pos)
            return

        b = self.board

        if b.round + self.power_depth - depth == b.piece_num * b.piece_num : # board is full
            return

        # for every position in optimal search set, try to move this piece and expand to deeper depth
        # if the expansion is at least as good as existing ones, keep it (which is next_search_set) and call minimax recursively on it
        for (r, c) in search_set: 

            if (self.power_depth - depth) % 2:
                b.grid[r][c] = self.color
                self.dict = self.my_dict
            else:
                b.grid[r][c] = self.opponent_color
                self.dict = self.op_dict
            self.notify_my_neighbor(r, c)

            if self.board.debug_delay > 0:
                self.board.r_grid[r][c] = - (self.board.round + self.power_depth - depth)
                self.board.trace_grid[r][c] = min(self.board.trace_grid[r][c], self.power_depth - depth)
                self.board.draw()
                pg.time.delay(self.board.debug_delay)

            # conf = self.dict_grid[r][c]
            # if len(conf) == 10 and conf[0] == 'm' and conf[9] == '+':
            #     print("grab defensive attack move", r, c)
            #     self.final_pos = (r, c)
            #     return

            next_search_set = self.fetch_optimal_search_set(pos_list, conf_list, eval_list, depth - 1, width, is_naive)

            if len(next_search_set) == 0:
                pos_list[depth].remove((r, c))
            else:
                # print("at depth", depth, "with position", r, c, "next search list size is", len(next_search_set))
                if len(search_set) > 1:
                    if (self.power_depth - depth) % 2:
                        if eval_list[depth][0] <= 5 and eval_list[depth][0] > 2:
                            self.minimax(next_search_set, pos_list, conf_list, eval_list, depth - 1, width, is_naive)
                    else:
                        if eval_list[depth][0] <= 5:
                            self.minimax(next_search_set, pos_list, conf_list, eval_list, depth - 1, width, is_naive)

            b.grid[r][c] = 0
            self.notify_my_neighbor(r, c)

            if self.board.debug_delay > 0:
                self.board.r_grid[r][c] = 0
                self.board.draw()
                pg.time.delay(self.board.debug_delay)

    # if !is_naive, fetch all empty neighbors within width that has the lowest rank, else fetch those with the lowest rank and highest score
    # output: optimal_search_set
    def fetch_optimal_search_set(self, pos_list, conf_list, eval_list, depth, width, is_naive):
        
        ret = set()
        maxPos = None
        maxConf = 'alpha'
        maxEval = self.dict['alpha'] # the current maximum configuration we can get at current depth and width
        b = self.board
        for r in range(b.piece_num):
            for c in range(b.piece_num):
                if b.grid[r][c] != 0: # fetch filled cell
                    continue
                for i in range(max(r - width, 0), min(r + width + 1, b.piece_num)):
                    for j in range(max(c - width, 0), min(c + width + 1, b.piece_num)):
                        if b.grid[i][j] == 0: # fetch empty neighbors of filled cell
                            eval = self.h_grid[i][j]
                            if is_naive:
                                if eval[0] < maxEval[0] or (eval[0] == maxEval[0] and eval[1] > maxEval[1]):
                                    maxPos = (i, j)
                                    maxConf = self.dict_grid[i][j]
                                    maxEval = eval
                                    #for p in range(0, depth + 1):
                                    #    pos_list[p].clear()
                                    ret.clear()
                                    ret.add((i, j))
                                elif eval == maxEval:
                                    ret.add((i, j))
                            else:
                                if eval[0] < maxEval[0]:
                                    maxPos = (i, j)
                                    maxConf = self.dict_grid[i][j]
                                    maxEval = eval
                                    #for p in range(0, depth + 1):
                                    #    pos_list[p].clear()
                                    ret.clear()
                                    ret.add((i, j))
                                elif eval[0] == maxEval[0]:
                                    ret.add((i, j))
        if len(ret) == 0:
            return ret

        if (self.power_depth - depth) % 2:
            # my turn, the current max configuration needs to be at least as good as my known moves, or else erase it
            if is_naive:
                if maxEval[0] < eval_list[depth][0] or (maxEval[0] == eval_list[depth][0] and maxEval[1] > eval_list[depth][1]):
                    for p in range(0, depth + 1):
                        pos_list[p].clear()
                if maxEval[0] > eval_list[depth][0] or (maxEval[0] == eval_list[depth][0] and maxEval[1] < eval_list[depth][1]):
                    ret.clear()
                else:
                    for pos in ret:
                        pos_list[depth].add(pos)
                    conf_list[depth] = maxConf
                    eval_list[depth] = maxEval
            else:
                if maxEval[0] < eval_list[depth][0]:
                    for p in range(0, depth + 1):
                        pos_list[p].clear()
                if maxEval[0] > eval_list[depth][0]:
                    ret.clear()
                else:
                    for pos in ret:
                        pos_list[depth].add(pos)
                    conf_list[depth] = maxConf
                    eval_list[depth] = maxEval
        else:
            # opponent turn, the current max configuration needs to be at least as worse as their known moves, or else erase it
            # use self.dict_grid, always piroritize "my" move than "opponent" move, because opponent is move-restricted if it chooses to defend
            # instead of attacking, if the defense is more dense (i.e. rank lower), it is priroritized, otherwise if it attacks, 
            # higher rank is preferred, i.e. its attack is weaker

            # base case
            if conf_list[depth] == 'beta':
                for pos in ret:
                    pos_list[depth].add(pos)
                conf_list[depth] = maxConf
                eval_list[depth] = maxEval
                return ret
            # current move is aggressive, discard it
            elif (maxConf[0] == 'o' and conf_list[depth][0] != 'o'):
                ret.clear()
                return ret
            # both moves aggressive, compare and choose the one with higher rank
            elif maxConf[0] == 'o':
                if is_naive:
                    if maxEval[0] > eval_list[depth][0] or (maxEval[0] == eval_list[depth][0] and maxEval[1] < eval_list[depth][1]):
                        for p in range(0, depth + 1):
                            pos_list[p].clear()
                    if maxEval[0] < eval_list[depth][0] or (maxEval[0] == eval_list[depth][0] and maxEval[1] > eval_list[depth][1]):
                        ret.clear()
                    else:
                        for pos in ret:
                            pos_list[depth].add(pos)
                        conf_list[depth] = maxConf
                        eval_list[depth] = maxEval
                else:
                    if maxEval[0] > eval_list[depth][0]:
                        for p in range(0, depth + 1):
                            pos_list[p].clear()
                    if maxEval[0] < eval_list[depth][0]:
                        ret.clear()
                    else:
                        for pos in ret:
                            pos_list[depth].add(pos)
                        conf_list[depth] = maxConf
                        eval_list[depth] = maxEval
            # cur move defensive, want this
            elif (maxConf[0] != 'o' and conf_list[depth][0] == 'o') or (maxConf[0] != 'o' and maxConf[0] != 'm'):
                for p in range(0, depth + 1):
                    pos_list[p].clear()
                for pos in ret:
                    pos_list[depth].add(pos)
                conf_list[depth] = maxConf
                eval_list[depth] = maxEval
                return ret
            # best move is random, want this
            elif conf_list[depth][0] != 'm':
                ret.clear()
                return ret
            # both move defensive, choose the one with lower rank
            else:
                if is_naive:
                    if maxEval[0] < eval_list[depth][0] or (maxEval[0] == eval_list[depth][0] and maxEval[1] > eval_list[depth][1]):
                        for p in range(0, depth + 1):
                            pos_list[p].clear()
                    if maxEval[0] > eval_list[depth][0] or (maxEval[0] == eval_list[depth][0] and maxEval[1] < eval_list[depth][1]):
                        ret.clear()
                    else:
                        for pos in ret:
                            pos_list[depth].add(pos)
                        conf_list[depth] = maxConf
                        eval_list[depth] = maxEval
                else:
                    if maxEval[0] < eval_list[depth][0]:
                        for p in range(0, depth + 1):
                            pos_list[p].clear()
                    if maxEval[0] > eval_list[depth][0]:
                        ret.clear()
                    else:
                        for pos in ret:
                            pos_list[depth].add(pos)
                        conf_list[depth] = maxConf
                        eval_list[depth] = maxEval  
        return ret

    # get max (conf, regularized_score) from 2 (conf, regularized_score), sometimes rank needs to upgrade to enforce moves (i.e. rank 4 -> 3)
    # regularized_score is what previous conf left over
    # add these score up in the end (in method update_heuristic)
    # we do NOT add score here since we want to keep the conf as the way it is, we do not want things like "my open 3+3+3" to be missed so conf is needed instead of just (rank, score)
    def get_maxh(self, cs1, cs2):

        (conf1, s1) = cs1
        (conf2, s2) = cs2
        h1 = self.dict[conf1]
        h2 = self.dict[conf2]
        s = s1 + s2

        if h1[0] < h2[0]: # if rank differs, emit the LOWER conf and add score of HIGHER conf to regularized_score
            return (conf1, h2[1] + s)
        elif h1[0] > h2[0]:
            return (conf2, h1[1] + s)
        else: # same rank, upgraded conf does not has regularized_score because it is explicitly dealt during the upgrade
            # rank 4 -> rank 3 (for now, may change rank later)
            if h1[0] == self.dict['my open 3'][0]:
                if conf1 == 'my open 3' and conf2 == conf1: # 2 my open 3
                    # print('my open 3+3 detected')
                    return ('my open 3+3', 0)
                elif conf1[0] == 'm' and conf2[0] == conf1: # at least 1 my open 3
                    # print('my open 3+4 detected')
                    return ('my open 3+4', 0)
                elif conf1 == 'op open 3' and (conf2 == 'op sleep 4' or conf2 == 'op sep 5'): # this is killer move, rank upgrade
                    # print('op open 3+4 detected')
                    return ('op open 3+4', 0)
                elif conf1[0] == 'o' and conf2[0] == 'o': # otherwise just emit the score change, rank does NOT change
                    # print('op open 3+3 detected')
                    return ('op open 3+3', 0)
                else:
                    return (conf1, h2[1] + s)
            # to implement: check if other rank needs to upgrade
            # elif (...):
            else: # do normal stuff 
                return (conf1, h2[1] + s)
            return (conf1, h2[1] + s)

    """
    AI 1.0: one step with rank + score
    """
    def move_piece_1(self): # move the one with highest rank and score, if there are multiple ones, choose "randomly"

        b = self.board
        ret_r = b.piece_num // 2 - 1 # the optimal row
        ret_c = b.piece_num // 2 - 1 # the optimal col
        r_list = [ret_r] # a list stores all the "optimal" rows
        c_list = [ret_c] # a list stores all the "optimal" cols
        hmax = self.dict['alpha']
        for r in range(b.piece_num):
            for c in range(b.piece_num):
                if self.h_grid[r][c][0] == -1:
                    continue
                elif self.h_grid[r][c][0] < hmax[0] or (self.h_grid[r][c][0] == hmax[0] and self.h_grid[r][c][1] > hmax[1]): # choose LOWER rank and higher score
                    hmax = self.h_grid[r][c]
                    ret_r = r
                    ret_c = c
                    r_list = [ret_r]
                    c_list = [ret_c]
                elif self.h_grid[r][c] == hmax: # same rank and score
                    r_list.append(r)
                    c_list.append(c)

        if hmax == self.dict['beta']: # all cells filled
            return (-10, -10) # special place to denote that the game is draw

        """
        Improve this randomness by searching deeper, i.e. modified minimax
        """
        rand_choice = random.randint(0, len(r_list) - 1) # randomly choose one "optimal" move
        # print("the optimal list length is", len(r_list), "the choice is", rand_choice, "with h =", hmax)
        ret_r = r_list[rand_choice]
        ret_c = c_list[rand_choice]

        return (ret_r, ret_c)

    """
    DISCARDED because now score sync with rank anyway...and this result becomes useless
    AI 0.5: one step with score
    """
    def move_piece_0_5(self): # move the one with highest score, if there are multiple ones, choose "randomly"

        b = self.board
        ret_r = b.piece_num // 2 - 1 # the optimal row
        ret_c = b.piece_num // 2 - 1 # the optimal col
        r_list = [ret_r] # a list stores all the "optimal" rows
        c_list = [ret_c] # a list stores all the "optimal" cols
        hmax = -100
        for r in range(b.piece_num):
            for c in range(b.piece_num):
                if self.h_grid[r][c][0] == -1:
                    continue
                elif self.h_grid[r][c][1] > hmax: # choose higher score
                    hmax = self.h_grid[r][c][1]
                    ret_r = r
                    ret_c = c
                    r_list = [ret_r]
                    c_list = [ret_c]
                elif self.h_grid[r][c][1] == hmax: # same score
                    r_list.append(r)
                    c_list.append(c)

        if hmax == -100: # all cells filled
            return (-10, -10) # speical place to denote that the game is draw

        """
        Improve this randomness by searching deeper, i.e. modified minimax
        """
        rand_choice = random.randint(0, len(r_list) - 1) # randomly choose one "optimal" move
        # print("the optimal list length is", len(r_list), "the choice is", rand_choice, "with h =", hmax)
        ret_r = r_list[rand_choice]
        ret_c = c_list[rand_choice]

        return (ret_r, ret_c)

    """
    AI 0.0: one step with rank
    """
    def move_piece_0(self): # move the one with highest rank, if there are multiple ones, choose "randomly"

        b = self.board
        ret_r = b.piece_num // 2 - 1 # the optimal row
        ret_c = b.piece_num // 2 - 1 # the optimal col
        r_list = [ret_r] # a list stores all the "optimal" rows
        c_list = [ret_c] # a list stores all the "optimal" cols
        hmax = self.dict['alpha']
        for r in range(b.piece_num):
            for c in range(b.piece_num):
                if self.h_grid[r][c][0] == -1:
                    continue
                elif self.h_grid[r][c][0] < hmax[0]: # choose LOWER rank and higher score
                    hmax = self.h_grid[r][c]
                    ret_r = r
                    ret_c = c
                    r_list = [ret_r]
                    c_list = [ret_c]
                elif self.h_grid[r][c][0] == hmax[0]: # same rank
                    r_list.append(r)
                    c_list.append(c)

        if hmax == self.dict['beta']: # all cells filled
            return (-10, -10) # speical place to denote that the game is draw

        """
        Improve this randomness by searching deeper, i.e. modified minimax
        """
        rand_choice = random.randint(0, len(r_list) - 1) # randomly choose one "optimal" move
        # print("the optimal list length is", len(r_list), "the choice is", rand_choice, "with h =", hmax)
        ret_r = r_list[rand_choice]
        ret_c = c_list[rand_choice]

        return (ret_r, ret_c)

    """
    A heuristic for each piece by observing its neighborhood, the final (rank, score) is updated in h_grid
    """
    def update_heuristic(self, r, c):

        b = self.board
        if b.grid[r][c] != 0:
            self.h_grid[r][c] = (-1, 0) # if piece already placed, rank = -1
            return

        # get all direction (configurations, regularized_score)
        cs1 = self.calculate_heuristic(self.count_continuous_piece(r, c, -1, 0), self.count_continuous_piece(r, c, 1, 0), r, c, ((-1, 0), (1, 0)))
        cs2 = self.calculate_heuristic(self.count_continuous_piece(r, c, 0, -1), self.count_continuous_piece(r, c, 0, 1), r, c, ((0, -1), (0, 1)))
        cs3 = self.calculate_heuristic(self.count_continuous_piece(r, c, -1, -1), self.count_continuous_piece(r, c, 1, 1), r, c, ((-1, -1), (1, 1)))
        cs4 = self.calculate_heuristic(self.count_continuous_piece(r, c, -1, 1), self.count_continuous_piece(r, c, 1, -1), r, c, ((-1, 1), (1, -1)))

        if not ((cs1[0] in self.dict) and (cs2[0] in self.dict) and (cs3[0] in self.dict) and (cs4[0] in self.dict)):
            print("No such configuration from:", cs1[0], cs2[0], cs3[0], cs4[0])
            raise NotImplementedError

        (conf, regularized_score) = self.get_maxh(self.get_maxh(cs1, cs2), self.get_maxh(cs3, cs4))

        self.dict_grid[r][c] = conf
        self.h_grid[r][c] = (self.dict[conf][0], self.dict[conf][1] + regularized_score)

    """
    based on left and right side of neighborhood, choose heuristic
    input: 2 x (continuous color, if end is blocked, continuous number), position r and c, direction left and right
    output: (the current piece's configuration in h_dictionary, regularized_score)
    useful combo: (left/right[0] == 0 and left/right[1]) => wall
                  (left/right[0] == 0 and not left/right[1]) => open
    ?: {
        X: me
        O: opponent
        C: current position
        _: open
        |: blocked (either by opponent or wall, does not matter)
        .: unknown / ignored
        }
    ?+ / +?: one or multiples of ?

    """
    def calculate_heuristic(self, left, right, r, c, direction):

        # left is me, right is me
        # based on current setup, it is actually possible to do look ahead of this situation by count_open_continuous_piece as well,
        # but we will leave that to minimax to handle, or else..."1 step" just becomes too powerful, which is not intended
        if self.color == left[0] and self.color == right[0]:
            continuous_num = left[2] + right[2] + 1
            if left[1] or right[1]: # blocked at least one side
                h = self.get_my_blocked_heuristic(left[1] and right[1], continuous_num)
                return (h, 0)
            else:
                h = self.get_my_open_heuristic(continuous_num)
                return (h, 0)

        # left is me, right is opponent
        elif self.color == left[0] and self.opponent_color == right[0]:
            h1 = self.get_my_blocked_heuristic(left[1], left[2] + 1) 
            h2 = self.get_opponent_blocked_heuristic(right[1], right[2] + 1)
            return self.get_maxh((h1, 0), (h2, 0))

        # left is me, right is open
        elif self.color == left[0] and right[0] == 0 and not right[1]: # this is the flipped one of "left is open, right is me", both needs to be modified in the flipped way, if needed
            continuous_num = left[2] + 1
            (open_color, open_end_blocked, open_continuous_num) = self.count_open_continuous_piece(r, c, direction[1][0], direction[1][1])
            if left[1]:
                if open_color == self.opponent_color or (open_color == 0 and open_end_blocked): # in the form of "...|+XC_|..."
                    if continuous_num == 5: # winning 5, rank 1
                        # print("winning 5, attack!")
                        return ('my win 5', 0)
                    elif continuous_num == 4: # sleep 4, forcing move as rank 3
                        return ('my sleep 4', 0)
                    else: # dead end
                        return ('my dead', 0)
                elif open_color == self.color: # in the form of "...|+XC_X..."
                    treat_as_continuous_num = continuous_num + open_continuous_num
                    if treat_as_continuous_num >= 4: # sep 5 or more, forcing move as rank 3
                        return ('my sep 5', 0)
                    elif treat_as_continuous_num == 3: # sep 4
                        if open_end_blocked: # dead end
                            return ('my dead', 0)
                        else:
                            return ('my sleep 3', 0) # = h(my sleep 3)
                    else: # too few pieces, do normal stuff
                        h = self.get_my_blocked_heuristic(False, continuous_num)
                        return (h, 0)
                else: # open ended, do normal stuff
                    h = self.get_my_blocked_heuristic(False, continuous_num)
                    return (h, 0)
            else:
                if open_color == self.opponent_color: # in the form of "..._+XC_O..."
                    if continuous_num >= 4: # in the form of "..._+XXXC_O...", winning move guaranteed, consider as "open continuous_num" directly
                        h = self.get_my_open_heuristic(continuous_num)
                        return (h, 0)
                    elif continuous_num == 3: # in the form of "..._XXC_O...", it is "aggressive", but opponent would block left almost guaranteed, not a very good move
                        h = self.get_my_open_heuristic(continuous_num)
                        return (h, 0)
                    elif continuous_num <= 2: # in the form of "..._XC_O" or "..._C_O"
                        h = self.get_my_open_heuristic(continuous_num)
                        return (h, 0)
                elif open_color == self.color: # in the form of "..._+XC_X+..."
                    if continuous_num >= 4: # in the form of "..._+XXXC_X+...", same as winning 4, rank 3
                        h = self.get_my_open_heuristic(continuous_num)
                        return (h, 0)
                    elif continuous_num == 3: # in the form of "..._XXC_X+..." very aggressive, forcing move as rank 3
                        h = self.get_my_open_heuristic(continuous_num)
                        return (h, 0)
                    elif not open_end_blocked: # in the form of "..._+XC_X+_..."
                        treat_as_continuous_num = continuous_num + open_continuous_num # treat as these continuous num
                        if treat_as_continuous_num >= 4: # sep 5 or more, forcing move as rank 3
                            return ('my sep 5', 0)
                        elif treat_as_continuous_num == 3: # sep 4 in the form of "..._XC_X_...", forcing move as rank 3
                            return ('my sep 4', 0) # make this same as above for now, since "...XXX_X..."or "...XX_X" actually does not make a difference, except they forces different moves
                        else: # this should not happen since we guarantees X on both sides
                            print("WARNING: unexpected sep 3")
                            return ('my sep 3', 0)
                    else: # in the form of "..._+XC_X+|..."
                        h = self.get_my_open_heuristic(continuous_num)
                        return (h, 0)
                elif open_end_blocked: # in the form of "..._+XC_|", do normal stuff
                    h = self.get_my_open_heuristic(continuous_num)
                    return (h, 0)
                else: # in the form of "..._+XC__", do normal stuff
                    h = self.get_my_open_heuristic(continuous_num)
                    return (h, 0)

        # left is me, right is wall
        elif self.color == left[0] and right[0] == 0 and right[1]:
            if left[1]:
                if left[2] + 1 >= 5:
                    # print("winning 5, attack!")
                    return ('my win 5', 0)
                else:
                    return ('my dead', 0)
            else:
                h = self.get_my_blocked_heuristic(False, left[2] + 1)
                return (h, 0)

        # left is opponent, right is opponent
        elif self.opponent_color == left[0] and self.opponent_color == right[0]:
            continuous_num = left[2] + right[2] + 1
            if left[1] or right[1]: # blocked at least one side
                h = self.get_opponent_blocked_heuristic(left[1] and right[1], continuous_num)
                return (h, 0)
            else:
                h = self.get_opponent_open_heuristic(continuous_num)
                return (h, 0)

        # left is opponent, right is me
        elif self.opponent_color == left[0] and self.color == right[0]:
            h1 = self.get_opponent_blocked_heuristic(left[1], left[2] + 1) 
            h2 = self.get_my_blocked_heuristic(right[1], right[2] + 1)
            return self.get_maxh((h1, 0), (h2, 0))

        # left is opponent, right is open
        elif self.opponent_color == left[0] and right[0] == 0 and not right[1]: # this is the flipped one of "left is open, right is opponent", both needs to be modified in the flipped way, if needed
            continuous_num = left[2] + 1
            (open_color, open_end_blocked, open_continuous_num) = self.count_open_continuous_piece(r, c, direction[1][0], direction[1][1])
            if left[1]: # in the form of "...|+OC_..."
                if open_color == self.opponent_color: # in the form of "...|+OC_O+..."
                    treat_as_continuous_num = continuous_num + open_continuous_num
                    if continuous_num >= 5: # if left side is already winning 5
                        return ('op win 5', 0)
                    elif open_end_blocked: # in the form of "...|+OC_O+|...", it depends if current position is good to me, because it is not necessarily to block right now, unless we are actually fear about the forcing move incoming on C or _
                        return ('op sleep 3', 0) # for now, = h(sleep 3)
                    else: # in the form of "...|+OC_O+_...", denoted as <1>
                        if treat_as_continuous_num >= 4: # otherise treat as 4, since even if it is 5 or more, there is space in between, forcing move as rank 4
                            h = self.get_opponent_blocked_heuristic(False, 4)
                            return (h, 0)
                        else: # otherwise do it as the sum of both sides
                            h = self.get_opponent_blocked_heuristic(False, treat_as_continuous_num)
                            return (h, 0)
                elif open_color == self.color or (open_color == 0 and open_end_blocked): # in the form of "...|+OC_|..."
                    if continuous_num >= 5: # winning 5
                        return ('op win 5', 0)
                    elif continuous_num == 4: # same as sleep 4
                        return ('op sleep 4', 0)
                    else: # dead end
                        return ('op dead', 0)
                else: # in the form of "...|+OC__", do the normal stuff
                    h = self.get_opponent_blocked_heuristic(False, continuous_num)
                    return (h, 0)
            else: # in the form of "..._+OC_..."
                if open_color == self.opponent_color: # in the form of "..._+OC_O+..."
                    treat_as_continuous_num = continuous_num + open_continuous_num
                    if open_end_blocked: # in the form of "..._+OC_O+|...", similar to "...|+O_CO+_...", i.e. the flipped one like <1>
                        if continuous_num >= 5: # I would be lost the next round if this is the case, opponent open 5 as rank 2, need to win right now
                            return ('op win 5', 0)
                        elif continuous_num == 4: # opponent open 4 or sleep 4, forcing move as rank 4
                            return ('op open 4', 0)
                        elif open_continuous_num == 4: # remember, we are blocking at C, if the right is sleep 4, we do NOT want to move to C at all, since it may take over the forcing move point
                            return ('op dead', 0)
                        elif treat_as_continuous_num >= 4: # otherwise treat as sleep 4, since now we count the right side as a whole to the left
                            return ('op sleep 4', 0)
                        else: # otherwise we are left with sleep 3 as the only choice
                            return ('op sleep 3', 0)
                    else: # in the form of "...+OC_O+_..."
                        if continuous_num >= 5: # same as before, if these conditions are held, ignore the right and do normal blocking
                            return ('op win 5', 0)
                        elif continuous_num == 4: # same as before
                            return ('op open 4', 0)
                        elif open_continuous_num >= 3: # same as before
                            return ('op dead', 0)
                        else: # sep 4, treat as forcing move as rank 4, example forms are "..._OC_O_...", "..._OC_OO_...", "..._OOC_O_..." and more
                            return ('op sep 4', 0)
                elif open_color == self.color or (open_color == 0 and open_end_blocked): # in the form of "...+OC_O+|...", ignore right for now
                    h = self.get_opponent_open_heuristic(continuous_num)
                    return (h, 0)
                else: # in the form of "...+OC__..."
                    h = self.get_opponent_open_heuristic(continuous_num)
                    return (h, 0)

        # left is opponent, right is wall
        elif self.opponent_color == left[0] and right[0] == 0 and right[1]:
            if left[1]:
                if left[2] + 1 >= 5:
                    # print("winning 5, defence!")
                    return ('op win 5', 0)
                else:
                    return ('op dead', 0)
            else:
                h = self.get_opponent_blocked_heuristic(False, left[2] + 1)
                return (h, 0)

        # left is open, right is me
        elif left[0] == 0 and not left[1] and self.color == right[0]: # this is almost a copy of the flipped one but still need some minor changes
            continuous_num = right[2] + 1
            (open_color, open_end_blocked, open_continuous_num) = self.count_open_continuous_piece(r, c, direction[0][0], direction[0][1])
            if right[1]:
                if open_color == self.opponent_color or (open_color == 0 and open_end_blocked): # in the form of "...|_CX+|..."
                    if continuous_num == 5: # winning 5, rank 1
                        # print("winning 5, attack!")
                        return ('my win 5', 0)
                    elif continuous_num == 4: # sleep 4, forcing move as rank 3
                        return ('my sleep 4', 0)
                    else: # dead end
                        return ('my dead', 0)
                elif open_color == self.color: # in the form of "...X_CX+|..."
                    treat_as_continuous_num = continuous_num + open_continuous_num
                    if treat_as_continuous_num >= 4: # sep 5 or more, forcing move as rank 3
                        return ('my sep 5', 0)
                    elif treat_as_continuous_num == 3: # sep 4
                        if open_end_blocked: # dead end
                            return ('my dead', 0)
                        else:
                            return ('my sleep 3', 0) # = h(my sleep 3)
                    else: # too few pieces, do normal stuff
                        h = self.get_my_blocked_heuristic(False, continuous_num)
                        return (h, 0)
                else: # open ended, do normal stuff
                    h = self.get_my_blocked_heuristic(False, continuous_num)
                    return (h, 0)
            else:
                if open_color == self.opponent_color: # in the form of "...+O_CX+_..."
                    if continuous_num >= 4: # in the form of "...+O_CXXX+_...", winning move guaranteed, consider as "open continuous_num" directly
                        h = self.get_my_open_heuristic(continuous_num)
                        return (h, 0)
                    elif continuous_num == 3: # in the form of "...+O_CXX_...", it is "aggressive", but opponent would block left almost guaranteed, not a very good move
                        h = self.get_my_open_heuristic(continuous_num)
                        return (h, 0)
                    elif continuous_num <= 2: # in the form of "...+O_CX_..." or "...+O_C_..."
                        h = self.get_my_open_heuristic(continuous_num)
                        return (h, 0)
                elif open_color == self.color: # in the form of "...+X_CX+_..."
                    if continuous_num >= 4: # in the form of "...+X_CXXX+_...", same as winning 4, rank 3
                        h = self.get_my_open_heuristic(continuous_num)
                        return (h, 0)
                    elif continuous_num == 3: # in the form of ...+X_CXX_..." very aggressive, forcing move as rank 3
                        h = self.get_my_open_heuristic(continuous_num)
                        return (h, 0)
                    elif not open_end_blocked: # in the form of "..._+X_CX+_..."
                        treat_as_continuous_num = continuous_num + open_continuous_num # treat as these continuous num
                        if treat_as_continuous_num >= 4: # sep 5 or more, forcing move as rank 3
                            return ('my sep 5', 0)
                        elif treat_as_continuous_num == 3: # sep 4 in the form of "..._X_CX_...", forcing move as rank 3
                            return ('my sep 4', 0) # make this same as above for now, since "...X_XXX..."or "...X_XX" actually does not make a difference, except they forces different moves
                        else: # this should not happen since we guarantees X on both sides
                            print("WARNING: unexpected sep 3")
                            return ('my sep 3', 0)
                    else: # in the form of "...|+X_CX+_..."
                        h = self.get_my_open_heuristic(continuous_num)
                        return (h, 0)
                elif open_end_blocked: # in the form of "|_CX+_...", do normal stuff
                    h = self.get_my_open_heuristic(continuous_num)
                    return (h, 0)
                else: # in the form of "__CX+_...", do normal stuff
                    h = self.get_my_open_heuristic(continuous_num)
                    return (h, 0)

        # left is open, right is opponent
        elif left[0] == 0 and not left[1] and self.opponent_color == right[0]: # this is almost a copy of the flipped one but still need some minor changes
            continuous_num = right[2] + 1
            (open_color, open_end_blocked, open_continuous_num) = self.count_open_continuous_piece(r, c, direction[0][0], direction[0][1])
            if right[1]: # in the form of "..._CO+|..."
                if open_color == self.opponent_color: # in the form of "...+O_CO+|..."
                    treat_as_continuous_num = continuous_num + open_continuous_num
                    if continuous_num >= 5: # if left side is already winning 5
                        return ('op win 5', 0)
                    elif open_end_blocked: # in the form of "...|+O_CO+|...", it depends if current position is good to me, because it is not necessarily to block right now, unless we are actually fear about the forcing move incoming on C or _
                        return ('op sleep 3', 0) # for now, = h(sleep 3)
                    else: # in the form of "..._+O_CO+|...", denoted as <1>
                        if treat_as_continuous_num >= 4: # otherise treat as 4, since even if it is 5 or more, there is space in between, forcing move as rank 4
                            h = self.get_opponent_blocked_heuristic(False, 4)
                            return (h, 0)
                        else: # otherwise do it as the sum of both sides
                            h = self.get_opponent_blocked_heuristic(False, treat_as_continuous_num)
                            return (h, 0)
                elif open_color == self.color or (open_color == 0 and open_end_blocked): # in the form of "...|_CO+|..."
                    if continuous_num >= 5: # winning 5
                        return ('op win 5', 0)
                    elif continuous_num == 4: # same as sleep 4
                        return ('op sleep 4', 0)
                    else: # dead end
                        return ('op dead', 0)
                else: # in the form of "__CO+|...", do the normal stuff
                    h = self.get_opponent_blocked_heuristic(False, continuous_num)
                    return (h, 0)
            else: # in the form of "..._CO+_..."
                if open_color == self.opponent_color: # in the form of "...+O_CO+_..."
                    treat_as_continuous_num = continuous_num + open_continuous_num
                    if open_end_blocked: # in the form of "...|+O_CO+_...", similar to "..._+OC_O+|...", i.e. the flipped one like <1>
                        if continuous_num >= 5: # I would be lost the next round if this is the case, opponent open 5 as rank 2, need to win right now
                            return ('op win 5', 0)
                        elif continuous_num == 4: # opponent open 4 or sleep 4, forcing move as rank 4
                            return ('op open 4', 0)
                        elif open_continuous_num == 4: # remember, we are blocking at C, if the right is sleep 4, we do NOT want to move to C at all, since it may take over the forcing move point
                            return ('op dead', 0)
                        elif treat_as_continuous_num >= 4: # otherwise treat as sleep 4, since now we count the right side as a whole to the left
                            return ('op sleep 4', 0)
                        else: # otherwise we are left with sleep 3 as the only choice
                            return ('op sleep 3', 0)
                    else: # in the form of "..._+O_CO+..."
                        if continuous_num >= 5: # same as before, if these conditions are held, ignore the right and do normal blocking
                            return ('op win 5', 0)
                        elif continuous_num == 4: # same as before
                            return ('op open 4', 0)
                        elif open_continuous_num >= 3: # same as before
                            return ('op dead', 0)
                        else: # sep 4, treat as forcing move as rank 4, example forms are "..._O_CO_...", "..._OO_CO_...", "..._O_COO_..." and more
                            return ('op sep 4', 0)
                elif open_color == self.color or (open_color == 0 and open_end_blocked): # in the form of "...|+O_CO+...", ignore right for now
                    h = self.get_opponent_open_heuristic(continuous_num)
                    return (h, 0)
                else: # in the form of "...__CO+..."
                    h = self.get_opponent_open_heuristic(continuous_num)
                    return (h, 0)

        # left is open, right is wall
        elif left[0] == 0 and not left[1] and right[0] == 0 and right[1]:
            return ('wall', 0)

        # left is open, right is open
        elif left[0] == 0 and not left[1] and right[0] == 0 and not right[1]:
            return ('my open 1', 0)
        
        # left is wall, right is me
        elif left[0] == 0 and left[1] and self.color == right[0]:
            if right[1]:
                if right[2] + 1 >= 5:
                    # print("winning 5, attack!")
                    return ('my win 5', 0)
                else:
                    return ('my dead', 0)
            else:
                h = self.get_my_blocked_heuristic(False, right[2] + 1)
                return (h, 0)

        # left is wall, right is opponent
        elif left[0] == 0 and left[1] and self.opponent_color == right[0]:
            if right[1]:
                if right[2] + 1 >= 5:
                    # print("winning 5, defence!")
                    return ('op win 5', 0)
                else:
                    return ('op dead', 0)
            else:
                h = self.get_opponent_blocked_heuristic(False, right[2] + 1)
                return (h, 0)

        # left is wall, right is open
        elif left[0] == 0 and left[1] and right[0] == 0 and not right[1]:
            return ('wall', 0)

        # left is wall, right is wall
        elif left[0] == 0 and left[1] and right[0] == 0 and right[1]:
            return ('wall 2', 0)
        
        # should cover all cases
        print("left color:", left[0])
        print("left is_blocked:", left[1])
        print("right color:", right[0])
        print("right is_blocked:", right[1])
        raise NotImplementedError

    def get_opponent_open_heuristic(self, continuous_num):
        if continuous_num >= 5:
            # print("winning 5, defence!")
            return 'op win 5'
        elif continuous_num == 4:
            return 'op open 4'
        elif continuous_num == 3:
            return 'op open 3'
        elif continuous_num == 2:
            return 'op open 2'
        else:
            return 'op open 1'

    def get_opponent_blocked_heuristic(self, two_ends_blocked, continuous_num):
        if two_ends_blocked:
            if continuous_num >= 5: # winning 5
                # print("winning 5, defence!")
                return 'op win 5'
            else: # the other side is blocked by me, so this is a dead end
                return 'op dead'
        else:
            if continuous_num >= 5: # winning 5
                # print("winning 5, defence!")
                return 'op win 5'
            elif continuous_num == 4: # sleep 4
                return 'op sleep 4'
            elif continuous_num == 3: # sleep 3
                return 'op sleep 3'
            else: # does not care about opponent's sleep 2
                return 'op sleep 2'

    def get_my_open_heuristic(self, continuous_num):
        if continuous_num >= 5:
            # print("winning 5, attack!")
            return 'my win 5'
        elif continuous_num == 4: # open 4
            return 'my open 4'
        elif continuous_num == 3: # open 3
            return 'my open 3'
        elif continuous_num == 2: # open 2
            return 'my open 2'
        elif continuous_num == 1: # open 1
            return 'my open 1'
        else:
            raise NotImplementedError

    def get_my_blocked_heuristic(self, two_ends_blocked, continuous_num):
        if two_ends_blocked:
            if continuous_num >= 5: # winning 5
                # print("winning 5, attack!")
                return 'my win 5'
            else: # the other side is blocked by opponent, so this is a dead end
                return 'my dead'
        else:
            if continuous_num >= 5: # winning 5
                # print("winning 5, attack!")
                return 'my win 5'
            elif continuous_num == 4: # sleep 4
                return 'my sleep 4'
            elif continuous_num == 3: # sleep 3
                return 'my sleep 3'
            elif continuous_num == 2: # sleep 2
                return 'my sleep 2'
            else: # sleep 1, assign 1 for the initial few moves to be reasonably close
                return 'my sleep 1'

    # this is a wrapper for method "count_continuous_piece", where the current piece must be known to be OPEN
    def count_open_continuous_piece(self, r, c, dr, dc):

        b = self.board
        cur_r = r + dr
        cur_c = c + dc

        if not b.is_valid_pos(cur_r, cur_c): # current position out of range, consider as "blocked"
            return (0, True, 0)
        
        return self.count_continuous_piece(cur_r, cur_c, dr, dc)

    # different from board's method which only determines the winning state
    # count (continuous color, if end is blocked, continuous number)
    def count_continuous_piece(self, r, c, dr, dc):

        b = self.board
        cur_r = r + dr
        cur_c = c + dc

        if not b.is_valid_pos(cur_r, cur_c): # current position out of range, consider as "blocked"
            return (0, True, 0)
        
        color = b.grid[cur_r][cur_c]
        if color == 0: # current position is open, consider as "not blocked"
            return (0, False, 0)

        end_blocked = None
        continuous_num = 0
        open_heuristic = 0

        while True:
            if not b.is_valid_pos(cur_r, cur_c): # current position out of range, done
                end_blocked = True
                break
            elif b.grid[cur_r][cur_c] == color: # same color, increment continuous number and move to next position
                continuous_num += 1
                cur_r += dr
                cur_c += dc
            elif b.grid[cur_r][cur_c] == 0: # current position is open, done
                end_blocked = False
                break
            else: # current position is blocked by opponent, done
                end_blocked = True
                break

        return (color, end_blocked, continuous_num)

    """
    debug session
    """
    def print_h_board(self):

        for c in range(self.board.piece_num):
            for r in range(self.board.piece_num):
                print(self.h_grid[r][c], " " * (8 - len(str(self.h_grid[r][c]))), end = "")
            print()

    def print_rank_board(self):
        for c in range(self.board.piece_num):
            for r in range(self.board.piece_num):
                print(self.h_grid[r][c][0], " " * (5 - len(str(self.h_grid[r][c][0]))), end = "")
            print()

    def print_score_board(self):
        for c in range(self.board.piece_num):
            for r in range(self.board.piece_num):
                print(self.h_grid[r][c][1], " " * (5 - len(str(self.h_grid[r][c][1]))), end = "")
            print()
