# functions to get players 

def get_players(count=2):
    """ 
    Asks for player names and returns a list of players.

    """
    players = []
    for i in range(count):
        name = input(f"Enter name for player {i + 1}: ").strip() 
        players.append(name if name else f"Player {i + 1}")

    return players


