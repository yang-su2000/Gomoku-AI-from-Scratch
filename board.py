import pygame as pg # this is a global shared object now since board is included in every player's strategy
from pygame import gfxdraw # this is for smooth circle drawing

class Board:
    def __init__(self, debug_delay):

        self.piece_size = 30 # length of one piece
        self.piece_num = 18 # number of pieces per row / column
        self.start_r = 50 # top left index row
        self.start_c = 50 # top left index col
        self.toggle_range = self.piece_size / 2 # mouse toggle range for pygame
        self.board_size = self.piece_size * self.piece_num
        self.piece = 2 # the color of the current piece, 2 = black, 1 = white, 0 = None (empty)
        self.round = 0 # current round of the board
        self.show_round_num = True
        self.debug_delay = debug_delay
        self.winner = None
        self.gameover = False
        self.grid = [] # the board
        self.r_grid = [] # the round board
        self.trace_grid = [] # the trace board for visualization
        for i in range(self.piece_num):
            self.grid.append(list([0] * self.piece_num))
            self.r_grid.append(list([0] * self.piece_num))
            self.trace_grid.append(list([5] * self.piece_num))

        self.screen = pg.display.set_mode((700, 700))
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(u"C:\Windows\Fonts\Candarab.ttf", 24)
        self.font_small = pg.font.Font(u"C:\Windows\Fonts\Candarab.ttf", 16)

    def move_piece(self, r, c):

        if r == -10 and c == -10:
            self.gameover = True
            self.winner = 0
            print("Draw")
            return True

        if not self.is_valid_pos(r, c):
            print("Out of range")
            return False

        elif self.grid[r][c] != 0:
            print("Piece already set")
            return False

        self.grid[r][c] = self.piece
        self.round += 1
        self.r_grid[r][c] = self.round
        color = None
        if self.piece == 1:
            color = "White"
        elif self.piece == 2:
            color = "Black"
        if self.is_gameover(r, c):
            self.gameover = True
            # print(color, "wins!")
        else:
            print(color, "at", r, c)
            # self.print_board()
            pass
        return True

    def switch_player(self):
        if self.piece == 1:
            self.piece = 2
        elif self.piece == 2:
            self.piece = 1
        else:
            raise NO_SUCH_PIECE_ERROR

    def is_valid_pos(self, r, c):
        return r >= 0 and r < self.piece_num and c >= 0 and c < self.piece_num

    def is_gameover(self, r, c): # if yes, set gameover to True and declare the winner

        n_count = self.count_continuous_piece(r, c, -1, 0)
        s_count = self.count_continuous_piece(r, c, 1, 0)
        w_count = self.count_continuous_piece(r, c, 0, -1)
        e_count = self.count_continuous_piece(r, c, 0, 1)
        nw_count = self.count_continuous_piece(r, c, -1, -1)
        ne_count = self.count_continuous_piece(r, c, -1, 1)
        sw_count = self.count_continuous_piece(r, c, 1, -1)
        se_count = self.count_continuous_piece(r, c, 1, 1)

        if (n_count + s_count + 1 >= 5) or (e_count + w_count + 1 >= 5) or (se_count + nw_count + 1 >= 5) or (ne_count + sw_count + 1 >= 5):
            self.winner = self.grid[r][c]
            self.gameover = True

    def count_continuous_piece(self, r, c, dr, dc): # count the number of continuous piece in certain direction, not including yourself

        ret = 0
        color = self.grid[r][c]
        cur_r = r + dr
        cur_c = c + dc

        while (self.is_valid_pos(cur_r, cur_c)):
            if self.grid[cur_r][cur_c] == color:
                ret += 1
                cur_r += dr
                cur_c += dc
            else:
                return ret
        return ret

    def draw(self):

        self.screen.fill((255,255,255)) # background (white)
        self.screen.blit(self.font.render("FPS:{0:.2F}".format(self.clock.get_fps()), True, (0, 0, 0)), (10, 10)) # show FPS
        pg.draw.rect(self.screen, (185, 122, 87), [self.start_c - self.toggle_range, self.start_r - self.toggle_range, self.board_size, self.board_size], 0) # chessboard
        gfxdraw.aacircle(self.screen, self.board_size, self.piece_size // 2, self.piece_size // 2, (0, 0, 0)) # current player: black or white
        gfxdraw.filled_circle(self.screen, self.board_size, self.piece_size // 2, self.piece_size // 2, (0, 0, 0))
        gfxdraw.aacircle(self.screen, self.board_size, self.piece_size // 2, self.piece_size // 2 - 1, (0, 0, 0))
        gfxdraw.filled_circle(self.screen, self.board_size, self.piece_size // 2, self.piece_size // 2 - 1, (0, 0, 0) if self.piece == 2 else (255, 255, 255))

        for r in range(self.piece_num): # draw row lines
            cur_r = self.start_r + r * self.piece_size
            pg.draw.line(self.screen, (0, 0, 0), [self.start_r, cur_r], [self.start_r + self.piece_size * (self.piece_num - 1), cur_r], 2)

        for c in range(self.piece_num): # draw col lines
            cur_c = self.start_c + c * self.piece_size
            pg.draw.line(self.screen, (0, 0, 0), [cur_c, self.start_c], [cur_c, self.start_c + self.piece_size * (self.piece_num - 1)], 2)

        for r in range(self.piece_num): # draw pieces
            for c in range(self.piece_num):
                color = self.grid[r][c]
                round = self.r_grid[r][c]
                if color != 0: 
                    if color == 2: 
                        RGB = (0, 0, 0)
                    else:
                        RGB = (255, 255, 255)
                    cur_r = self.start_r + r * self.piece_size
                    cur_c = self.start_c + c * self.piece_size
                    gfxdraw.aacircle(self.screen, cur_r, cur_c, self.piece_size // 2, RGB) # antialiased filled shapes
                    gfxdraw.filled_circle(self.screen, cur_r, cur_c, self.piece_size // 2, RGB)
                    if self.show_round_num:
                        if round < 0:
                            self.screen.blit(self.font_small.render("{0}".format(- round), True, (255, 0, 0)), (cur_r - self.toggle_range // 2, cur_c - self.toggle_range / 2)) # show round number
                        else:
                            self.screen.blit(self.font_small.render("{0}".format(round), True, (255, 255, 255) if color == 2 else (0, 0, 0)), (cur_r - self.toggle_range // 2, cur_c - self.toggle_range / 2)) # show round number
                elif self.debug_delay > 0:
                    trace_color = self.trace_grid[r][c]
                    if trace_color < 5:
                        cur_r = self.start_r + r * self.piece_size
                        cur_c = self.start_c + c * self.piece_size
                        gfxdraw.aacircle(self.screen, cur_r, cur_c, self.piece_size // 6, (255, trace_color * 80 - 80, 0))
                        gfxdraw.filled_circle(self.screen, cur_r, cur_c, self.piece_size // 6, (255, trace_color * 80 - 80, 0))

        if self.gameover:
            gameover_text = None
            if self.winner == 2:
                gameover_text = "Black Win"
            elif self.winner == 1:
                gameover_text = "White Win"
            else:
                gameover_text = "Draw"
            self.screen.blit(self.font.render("{0}".format(gameover_text), True, (0, 0, 0)), (300, 10)) # show winner          
        pg.display.update()

    def print_board(self): # debug

        for c in range(self.piece_num):
            for r in range(self.piece_num):
                color = self.grid[r][c]
                if color == 0:
                    print("O", end = " ")
                elif color == 1:
                    print("W", end = " ")
                else:
                    print("B", end = " ")
            print()

    def print_r_board(self): # debug

        for c in range(self.piece_num):
            for r in range(self.piece_num):
                print(self.r_grid[r][c], " " * (3 - len(str(self.r_grid[r][c]))), end = "")
            print()