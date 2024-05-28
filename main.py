from rummikub import Rummikub
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--players",
                    choices = [2,3,4],
                    type = int,
                    default=2,
                    help = "Input a number between 2-4 for the number of players.")

def main():
    args = parser.parse_args()
    game = Rummikub(int(args.players))

    game.run_game()
    return

main()