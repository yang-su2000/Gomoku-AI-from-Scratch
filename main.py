from game import *

if __name__ == '__main__':
    # 1st param: (player_black, depth_level, width_level), for player_black, 1 = Computer, 0 = Human
    # 2nd param: (player_white, depth_level, width_level), for player_white, 1 = Computer, 0 = Human
    # 3rd param: delay (AI vs. AI only, unit: milliseconds, e.g. 500)
    # 4th param: debug mode delay (AI only, unit: milliseconds, e.g. 50, set to 0 to disable debug mode)
    # depth_level: AI only, number of steps AI thinks ahead
    # width_level: AI only, range of boards AI thinks of
    if 1: # for record
        MaxRuns = 100
        runs = 0
        black_wins = 0
        white_wins = 0
        draw = 0
        while runs < MaxRuns:
            game = Game((1, 6, 3), (1, 6, 3), 0, 1)
            game.game_loop()
            if game.board.winner == 2:
                black_wins += 1
            elif game.board.winner == 1:
                white_wins += 1
            else:
                draw += 1
            runs += 1
            print("black", black_wins, "white", white_wins, "draw", draw)
    else: # for testing
        game = Game((0, 1, 1), (1, 2, 3), 0, 50)
        game.game_loop()
