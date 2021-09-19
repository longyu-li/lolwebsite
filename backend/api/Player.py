

class Player:
    _player_id: str
    summoner_name: str
    region: str
    wins_on_team: int
    wins_on_enemy: int
    games_played_on_team: int
    games_played_on_enemy: int
    time_played: float

    def __init__(self, player_id: str, summoner_name: str, region: str):
        self._player_id = player_id
        self.summoner_name = summoner_name
        self.region = region
        self.wins_on_team = 0
        self.wins_on_enemy = 0
        self.games_played_on_team = 0
        self.games_played_on_enemy = 0
        self.time_played = 0.0

    def get_winrate_on_team(self) -> float:
        if self.games_played_on_team == 0:
            return 0.00
        return round(100 * (self.wins_on_team / self.games_played_on_team), 2)

    def get_winrate_on_enemy(self) -> float:
        if self.games_played_on_enemy == 0:
            return 0.00
        return round(100 * (self.wins_on_enemy / self.games_played_on_enemy), 2)

    def get_games_played_on_team(self) -> int:
        return self.games_played_on_team

    def get_total_games_played_on_enemy(self) -> int:
        return self.games_played_on_enemy

    def get_total_games_played(self) -> int:
        return self.games_played_on_team + self.games_played_on_enemy

    def get_hours_played(self) -> float:
        return round(self.time_played / 60000, 2)

    def played_on_team(self, has_won: bool, game_time: int) -> None:
        self.games_played_on_team += 1
        self.time_played += game_time
        if has_won:
            self.wins_on_team += 1

    def played_on_enemy(self, has_won: bool, game_time: int) -> None:
        self.games_played_on_enemy += 1
        self.time_played += game_time
        if has_won:
            self.wins_on_enemy += 1
