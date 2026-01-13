from .users import get_players

def play():
    """
    Tic Tac Toe game for two players.

    """

    players = get_players(2)
    board = [" "] * 9
    current = 0

    def show():
        for i in range(0, 9, 3):
            print(f" {board[i]} | {board[i+1]} | {board[i+2]} ")
            if i < 6:
                print("---+---+---")

    def win(symbol):
        combos = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        return any(board[a]==board[b]==board[c]==symbol for a,b,c in combos)
    
    symbols = ["X","O"]
    print("\n Tic Tac Toe Started")
    show()

    while True:
        try:
            move = int(input(f"{players[current]} ({symbols[current]}): ")) - 1
            if board[move] != " ":
                print("Position already filled...")
                continue
        except (ValueError,IndexError):
            print("Your move is invalid...")
            continue

        board[move] = symbols[current]
        show()

        if win(symbols[current]):
            print(f"Congratulations: {players[current]} wins....")
            break 

        if " " not in board:
            print(f"Draw...")
            break

        current = 1 - current
