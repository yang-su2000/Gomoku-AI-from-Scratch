from board import *

class Human:

    def __init__(self, is_black, board):

        self.color = 2 if is_black else 1 # constant
        self.board = board

    def final_move(self):

        b = self.board
        is_move = False
        mouse_pos = (-10, -10)

        while not is_move and not b.gameover:
            for event in pg.event.get():
                if event.type == pg.QUIT: # force quit
                    b.gameover = True
                elif event.type == pg.KEYDOWN and event.key == pg.K_q: # press q to quit game
                    b.gameover = True
                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    is_move = True # move piece
            b.draw()
            b.clock.tick(50)

        origin_r = b.start_r - b.toggle_range # visual top left index row
        origin_c = b.start_c - b.toggle_range # visual top left index col

        r = int((mouse_pos[0] - origin_r) / b.piece_size)
        c = int((mouse_pos[1] - origin_c) / b.piece_size)
        return (r, c)
