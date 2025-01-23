from rummikub.game import Game

if __name__ == "__main__":
    player_names = input("Enter player names (comma-separated): ").split(',')
    game = Game([name.strip() for name in player_names])
    game.start()

    while True:
        game.next_turn()