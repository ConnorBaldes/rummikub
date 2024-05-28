from player import Player
from table import Table


from termcolor import colored, cprint  # Import colored from termcolor module    
class Rummikub:
    def __init__(self, num_players):
        self.players = [Player(player_num) for player_num in range(num_players)]
        self.game_table = Table()


    def run_game(self):
        current_player_index = 0
        
        while not self.check_game_over():
            current_player = self.players[current_player_index]
            
            # Display game state and options to the current player
            self.display_game_state(current_player)
            options = self.get_player_options(current_player)
            
            # Take input from the current player
            action = self.get_player_input(current_player, options)
            
            # Execute the chosen action
            self.execute_action(current_player, action)
            
            # Move to the next player
            current_player_index = (current_player_index + 1) % len(self.players)
    
    def check_game_over(self):
        # Implement game-over condition here
        return False
    
    def display_game_state(self, player):
        
        #Display the rack of the players whos turn it currently is
        print(f"Your rack player {player.player_num}:")
        for tile in player.tile_rack:
            #check if a tile is a joker
            if tile[2] == 'joker':
                print(colored('J', 'white'), end=" ")
            else:
                # Use tile color to print colored value
                print(colored(tile[1], tile[2]), end=" ")

        print("\n")
        
        #Print the list of valid tile sets on the table
        print("Sets on the Table:")
        for tile_set in self.game_table.sets:
            for tile in tile_set:
                if tile[2] == 'joker':
                    print(colored('J', 'white'))
                else:
                    print(" ".colored(tile[1], tile[2]))
        
        return
    
    def get_player_options(self, player):
        # Determine available options for the player
        options = ["Take tile from pool"]
        return options
        
    
    def get_player_input(self, player, options):
        # Get input from the player
        print("Choose an action:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        choice = input("Enter the number of the action: ")
        while not choice.isdigit() or int(choice) not in range(1, len(options) + 1):
            choice = input("Invalid choice. Enter the number of the action: ")
        
        return options[int(choice) - 1]
    
    def execute_action(self, player, action):
        # Execute the chosen action
        if action == "Take tile from pool":
            # Take a tile from the table pool and place it in the player's hand
            tile = self.game_table.take_tile_from_pool()
            player.add_tile_to_rack(tile)