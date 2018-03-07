Environment:

    Python 3

Packages:

    time
    numpy

Classes n' Methods:

    Board()
        | copy(): copy itself
        | print_board(): print out
        | check_horizontal_state(): returns for example ['red', 'blue', 'red', '.', 'red']
        | check_vertical_state()
        | check_diag_1_state()
        | check_diag_2_state()
        | mark()
    
    Agent()
        | _all_valid_moves(): find all possible moves
        | win_lose_tie(): 'win' or 'lose' or 'tie' or 'UNFINISHED'
        | make_move(): move to a position
        | random_move()
