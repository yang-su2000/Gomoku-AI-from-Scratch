from human import *
from computer import *

class Game:

    def __init__(self, player_black, player_white, delay, debug_delay):

        pg.init()
        pg.display.set_caption("Gomoku (five-in-a-row)")
        self.run = True
        self.board = Board(debug_delay)
        self.black = player_black[0]
        self.white = player_white[0]
        self.player_black = Computer(True, self.board, player_black[1], player_black[2]) if self.black == 1 else Human(True, self.board)
        self.player_white = Computer(False, self.board, player_white[1], player_white[2]) if self.white == 1 else Human(False, self.board)
        self.delay = delay
        self.board.draw()

    def game_loop(self):

        while self.run:
            self.update()
            self.board.draw()
            self.board.switch_player()
            self.board.clock.tick(50)
        # self.quit()

    def update(self):

        for event in pg.event.get():
            if event.type == pg.QUIT: # force quit
                self.run = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_q: # press q to quit game
                self.run = False

        cur_color = self.board.piece
        # this "final_move" method is the only connection among players and the board, and it is also how every player's final decision on current step
        if cur_color == 2: # black's turn
            move = self.player_black.final_move()
        elif cur_color == 1: # white's turn
            move = self.player_white.final_move()

        if self.board.move_piece(move[0], move[1]):
            if cur_color == 2 and self.black == 1:
                self.player_black.notify_my_neighbor(move[0], move[1])
            elif cur_color == 1 and self.white == 1:
                self.player_white.notify_my_neighbor(move[0], move[1])
        else:
            self.run = False
            print("Invalid Move!")
        

        if self.board.gameover:
            self.run = False
        if self.black == self.white and self.black > 0: # if 2 AIs competing, delay a bit to make game watchable
            pg.time.delay(self.delay)

    def quit(self):

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT: # force quit
                    return
                elif event.type == pg.KEYDOWN and event.key == pg.K_q: # press q to quit game
                    return
