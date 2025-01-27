from game_board import GameBoard

x = GameBoard(amount_columns= 6, amount_rows= 7)
x.print_board()
x.play_move(1, "X")
x.print_board()
x.play_move(1, "P")
x.print_board()
