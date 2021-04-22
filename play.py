from game import *

if __name__ == '__main__':
    # 1st param: (player_black, depth_level, width_level), for player_black, 1 = Computer, 0 = Human
    # 2nd param: (player_white, depth_level, width_level), for player_white, 1 = Computer, 0 = Human
    # 3rd param: delay (AI vs. AI only, unit: milliseconds, e.g. 500)
    # 4th param: debug mode delay (AI only, unit: milliseconds, e.g. 50, set to 0 to disable debug mode)
    # depth_level: AI only, number of steps AI thinks ahead
    # width_level: AI only, range of boards AI thinks of
    
    player_black = None
    player_white = None
    black_depth = 1
    black_width = 1
    white_depth = 1
    white_width = 1
    delay = 0
    debug_delay = 0
    AI_level = [(-1, 0), (0, 0), (4, 3)]
    print() 
    print("    ,o888888o.        ,o888888o.              ,8.       ,8.              ,o888888o.     8 8888     ,88' 8 8888      88                    .8.           8 8888 ")
    print("   8888     `88.   . 8888     `88.           ,888.     ,888.          . 8888     `88.   8 8888    ,88'  8 8888      88                   .888.          8 8888 ")
    print(",8 8888       `8. ,8 8888       `8b         .`8888.   .`8888.        ,8 8888       `8b  8 8888   ,88'   8 8888      88                  :88888.         8 8888 ")
    print("88 8888           88 8888        `8b       ,8.`8888. ,8.`8888.       88 8888        `8b 8 8888  ,88'    8 8888      88                 . `88888.        8 8888 ")
    print("88 8888           88 8888         88      ,8'8.`8888,8^8.`8888.      88 8888         88 8 8888 ,88'     8 8888      88                .8. `88888.       8 8888 ")
    print("88 8888           88 8888         88     ,8' `8.`8888' `8.`8888.     88 8888         88 8 8888 88'      8 8888      88               .8`8. `88888.      8 8888 ")
    print("88 8888   8888888 88 8888        ,8P    ,8'   `8.`88'   `8.`8888.    88 8888        ,8P 8 888888<       8 8888      88              .8' `8. `88888.     8 8888 ")
    print("`8 8888       .8' `8 8888       ,8P    ,8'     `8.`'     `8.`8888.   `8 8888       ,8P  8 8888 `Y8.     ` 8888     ,8P             .8'   `8. `88888.    8 8888 ")
    print("   8888     ,88'   ` 8888     ,88'    ,8'       `8        `8.`8888.   ` 8888     ,88'   8 8888   `Y8.     8888   ,d8P             .888888888. `88888.   8 8888 ")
    print("    `8888888P'        `8888888P'     ,8'         `         `8.`8888.     `8888888P'     8 8888     `Y8.    `Y88888P'             .8'       `8. `88888.  8 8888 ")
    print()
    print("Welcome to Gomoku AI Version 0.2.3")
    tmp = None
    while tmp is None or (tmp != "1" and tmp != "0"):
        tmp = input("1/6 Choose Black, type 1 for AI or 0 for Human: ")
    player_black = 1 if tmp == "1" else 0
    tmp = None
    if player_black == 1:
        while tmp is None or (tmp != "0" and tmp != "1" and tmp != "2"): 
            tmp = input("2/6 Choose the AI level from 0 / 1 / 2: ")
        black_depth = AI_level[int(tmp)][0]
        black_width = AI_level[int(tmp)][1]
        tmp = None
    while tmp is None or (tmp != "1" and tmp != "0"):
        tmp = input("3/6 Choose White, type 1 for AI or 0 for Human: ")
    player_white = 1 if tmp == "1" else 0
    tmp = None
    if player_white == 1:
        while tmp is None or (tmp != "0" and tmp != "1" and tmp != "2"): 
            tmp = input("4/6 Choose the AI level from 0 / 1 / 2: ")
        white_depth = AI_level[int(tmp)][0]
        white_width = AI_level[int(tmp)][1]
        tmp = None
    tmp = input("5/6 Set the gameplay delay if AI is involved with range [1, 1000] or hit enter if no need: ")
    if tmp != "":
        delay = int(tmp)
    tmp = input("6/6 Set trace delay if AI is involved with range [1, 1000] or hit enter if not want trace: ")
    if tmp != "":
        debug_delay = int(tmp)
    print("Game Start!")
    game = Game((player_black, black_depth, black_width), (player_white, white_depth, white_width), delay, debug_delay)
    game.game_loop()