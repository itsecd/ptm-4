from dataclasses import dataclass, field
import logging
from typing import List, Dict


@dataclass
class Player:
    name: str
    position: str
    number: int
    goals: int = 0
    assists: int = 0

    def __str__(self):
        """
         All info about player
         
         @return string with all info about player
        """
        return (f"Player Info:\n"
            f"Name: {self.name}\n"
            f"Position: {self.position}\n"
            f"Number: {self.number}\n"
            f"Goals: {self.goals}\n"
            f"Assists: {self.assists}"
        )


@dataclass
class MatchResult:
    date: str
    outcome: str
    score: str
    opponent: str
    goal_scorers: List[str] = field(default_factory=list) 
    assist_givers: List[str] = field(default_factory=list)

    def __str__(self):
        """
         All info about match
         
         @return string with all info about player
        """
        return f"{self.outcome} against {self.opponent} with score {self.score}"


@dataclass
class FootballClub:
    name: str
    players: List[Player] = field(default_factory=list)
    match_results: Dict[str, MatchResult] = field(default_factory=dict)
    finances: float = 0.0
    scheduled_matches: List[Dict[str, str]] = field(default_factory=list)

    def __init__(self, name, finances=0.0):
        """
         Initializes the object with name and finances. 
         
         @param name - the name of the player
         @param finances - the number of finances 
        """
        self.name = name  
        self.players = []  
        self.match_results = {} 
        self.finances = finances  
        self.scheduled_matches = []
        self.logger = self.set_logger(self.name)

    def set_logger(self, name: str):
        """
         Sets up a logger to log to a file. 
         
         @param name - the name of the club, which will be logged
         
         @return the logger that was set up for this class
        """
        logger =  logging.getLogger("my_logger")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(f'{name}.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger

    def add_player(self, player: Player):
        """
         Adds a Player to the Club.
         
         @param player - all info about Player
         
         @return True - player was added 
                 False - Player number is already taken
        """
        if self._is_player_number_taken(player.number):
            logging.warning(f"Player number {player.number} is already taken.")
            return False
        self.players.append(player)
        self.logger.info(f"Player {player.name} added to the club.")
        return True

    def _is_player_number_taken(self, number: int) -> bool:
        """
         Checks if a player has already taken a given number.
         
         @param number - the number to check for
         
         @return True - the player has already taken the number 
                 False - the number is unoccupied
        """
        return any(player.number == number for player in self.players)

    def remove_player(self, name: str):
        """
         Removes a Player from club.
         
         @param name - name of player to remove
        """
        player_to_remove = next((player for player in self.players if player.name == name), None)
        
        if player_to_remove:
            self.players.remove(player_to_remove)
            self.logger.info(f"Player {name} removed from the club.")
        else:
            self.logger.warning(f"Can't remove player, because no player named '{name}' found in the club.")

    def record_match_result(self, match_result: MatchResult):
        """
         Record a match result.
         
         @param date - the date match was played.
         @param outcome - the outcome of the match. 
         @param score - number of goals scored
         @param opponent - team against which the match was played
        """
        self.match_results[match_result.date] = match_result
        self.logger.info(f"Match on {match_result.date}: {match_result} recorded.")

    def get_player_info(self, name: str):
        """
         Get information about a player. 
         
         @param player_name - name of the player
         
         @return The player with the given number or None if not found ( no player with that number is found in the
        """
        player = next((player for player in self.players if player.name == name), None)
        if player:
            self.logger.info(f"Info about {player.name} was requested")
            return f"Player Info:\nName: {player.name}\nPosition: {player.position}\nNumber: {player.number}\nGoals: {player.goals}\nAssists: {player.assists}"
        else:
            self.logger.warning(f"Can't get info about player, because no player named '{name}' found in the club.")
            return f"No player named '{name}' found in the club."

    def __str__(self):
        """
         All info about FootbalClub
         
         
         @return A string representation with All info about FootbalClub
        """
        player_count = len(self.players)
        return f"Football Club {self.name} with {player_count} player{'s' if player_count != 1 else ''}."

    def transfer_player(self, player_name: str, to_club: 'FootballClub', transfer_fee: float):
        """
         Transfer a player from one club to another.
         
         @param player_number - The player number to transfer. It must be in the range 0 to self. players. count - 1.
         @param to_club - The club to transfer the player to.
         @param transfer_fee - The amount of financial transferring.
         
         @return True - transfer is successful; 
                 False - transfer isn't successful.
        """
        player_to_transfer = next((player for player in self.players if player.name == player_name), None)
        if player_to_transfer and self._is_financial_transaction_valid(-transfer_fee):
            self._update_finances(-transfer_fee)
            to_club._update_finances(transfer_fee)
            self.players.remove(player_to_transfer)
            to_club.add_player(player_to_transfer)
            self.logger.info(f"Transferred {player_to_transfer.name} to {to_club.name} for ${transfer_fee}")
            return True
        else:
            self.logger.warning(f"Transfer failed for player {player_name}.")
            return False

    def _update_finances(self, amount: float):
        """
         Update finances by amount.
         
         @param amount - amount to add to the finances of the club.
        """
        self.finances += amount
        self.logger.info("Finances was updated.")

    def _is_financial_transaction_valid(self, amount: float) -> bool:
        """
         Checks if the financial transaction is valid.
         
         @param amount - The amount of funds to check.
         
         @return True - the transaction is valid;
                 False - the transaction isn't valid.
        """
        if self.finances + amount < 0:
            self.logger.warning("Insufficient funds for the transaction.")
            return False
        self.logger.info("Sufficient funds for the transaction.")
        return True

    def update_player_statistics(self, match_result: MatchResult):
        for player_name in match_result.goal_scorers:
            player = next((player for player in self.players if player.name == player_name), None)
            if player:
                player.goals += 1
                self.logger.info(f"{player.name} now has {player.goals} goal(s).")
            else:
                self.logger.warning(f"Player '{player_name}' not found in club {self.name}.")

        for player_name in match_result.assist_givers:
            player = next((player for player in self.players if player.name == player_name), None)
            if player:
                player.assists += 1
                self.logger.info(f"{player.name} now has {player.assists} assist(s).")
            else:
                self.logger.warning(f"Player '{player_name}' not found in club {self.name}.")


if __name__ == "__main__":
    club = FootballClub("FC Pythonistas", finances=1000000)

    player_john = Player("John Doe", "Forward", 9)
    player_jane = Player("Jane Smith", "Midfielder", 10)
    club.add_player(player_john)
    club.add_player(player_jane)

    match_result_1 = MatchResult(
        date="2023-11-25",
        outcome="Victory",
        score="2-0",
        opponent="FC Coders",
        goal_scorers=["John Doe", "Jane Smith"],
        assist_givers=["Jane Smith", "John Doe"]
    )

    club.record_match_result(match_result_1)

    match_result_2 = MatchResult(
        date="2023-12-01",
        outcome="Draw",
        score="1-1",
        opponent="FC Hackers",
        goal_scorers=["John Doe"],
        assist_givers=["Jane Smith"]
    )

    club.record_match_result(match_result_2)

    player_info = club.get_player_info("John Doe")
    club.remove_player("Jane Smith")

    club.update_player_statistics(match_result_1)
    club.update_player_statistics(match_result_2)

    club_B = FootballClub("FC Rival")
    club.transfer_player(player_john.number, club_B, 500000)
