from flask import Blueprint, jsonify, request
#from sqlalchemy.ext.declarative.api import as_declarative
from typing import Tuple, List, Dict
from .models import Summoner
from flask_cors import CORS
from typing import List
import requests



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


def get_player_id(summoner_name: str, region: str, key: str) -> str:
    response = requests.get("https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" +
                            summoner_name + "?api_key=" + key)
    i = 0
    while i < 5 and response.status_code != 200:
        response = requests.get("https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" +
                                summoner_name + "?api_key=" + key)
        i += 1
    if response.status_code == requests.codes.ok:
        return response.json()["puuid"]
    return ""


def get_recent_matches(pid: str, region: str, num_games: int, key: str) -> List[str]:
    response = requests.get("https://" + region + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + pid +
                            "/ids?start=0&count=" + str(num_games) + "&api_key=" + key)
    i = 0
    while i < 5 and response.status_code != 200:
        response = requests.get("https://" + region + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + pid +
                                "/ids?start=0&count=" + str(num_games) + "&api_key=" + key)
        i += 1
    if response.status_code == requests.codes.ok:
        return list(response.json())
    print(response)
    return []


def get_recent_players(player_id: str, match_ids: List[str], region: str, key: str) -> Dict[str, Player]:
    players = {}
    for match_id in match_ids:
        response = requests.get("https://" + region + ".api.riotgames.com/lol/match/v5/matches/" +
                                match_id + "?api_key=" + key)
        i = 0
        while i < 5 and response.status_code != 200:
            response = requests.get("https://" + region + ".api.riotgames.com/lol/match/v5/matches/" +
                                    match_id + "?api_key=" + key)
            i += 1
        if response.status_code == requests.codes.ok:
            team_id, has_won = get_team_id(player_id, response.json()["info"]["participants"])
            time_played = response.json()["info"]["gameDuration"]
            for participant in response.json()["info"]["participants"]:
                p_id = participant["puuid"]
                if p_id == player_id:
                    continue
                summoner_name = participant["summonerName"]
                players.setdefault(p_id, Player(p_id, summoner_name, region))
                if participant["teamId"] == team_id:
                    players[p_id].played_on_team(has_won, time_played)
                else:
                    players[p_id].played_on_enemy(not has_won, time_played)
    return players


def get_team_id(player_id: str, participants: list) -> Tuple[int, bool]:
    for participant in participants:
        if participant["puuid"] == player_id:
            return participant["teamId"], participant["win"]

APIKEY = "RGAPI-f52a40da-3658-464a-9227-a16e13f356bf"
regions = {"na1": "americas", "br1": "americas", "la1": "americas", "la2": "americas", "jp1": "asia",
           "kr": "asia", "oc1": "americas", "eun1": "europe", "euw1": "europe", "ru": "europe", "tr1": "europe"}


def run_api(summoner_name: str, region: str) -> List[Player]:
    
    pid = get_player_id(summoner_name, region, APIKEY)
    print("PRINT a")
    matches = get_recent_matches(pid, regions[region], 10, APIKEY)
    print("PRINT 1")
    recent_players = list(filter(lambda x: x.get_total_games_played() > 1,
                                 get_recent_players(pid, matches, regions[region], APIKEY).values()))
    print("PRINT 2")
    recent_players.sort(reverse=True, key=lambda player: player.get_total_games_played())
    print("PRINT 3")
    return recent_players



main = Blueprint('main', __name__)

@main.route('/<input_region>/<input_name>')
def search(input_region, input_name):
    #return "a", 201

    yes = run_api(input_name, input_region)
    if len(yes) == 0:
        return  {"to_return":"no one found"}, 201
    else :
        i = 0
        max_len = len(yes)
        while (i < max_len) :
            p = yes[i]
            yes[i] = "{} played {} games together with you for a total of {} minutes in the last 10 games.You have a {}% win rate together and {} has a {}% win rate against you.\n".format(p.summoner_name, p.get_total_games_played(), p.get_hours_played(), p.get_winrate_on_team(),p.summoner_name, p.get_winrate_on_enemy())
            i = i + 1
        to_return = tuple(yes)
        print(to_return)

    return {"to_return":to_return}, 201