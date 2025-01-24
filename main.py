from rummikub.game import Game

if __name__ == "__main__":
    while True:
        player_names = input("Enter player names (comma-separated, 2-4 players): ").split(',')
        player_names = [name.strip() for name in player_names]
        
        if 2 <= len(player_names) <= 4:
            break
        else:
            print("Invalid number of players! Please enter between 2 and 4 player names.")
    
    game = Game(player_names)
    game.start()

    while True:
        game.next_turn()
