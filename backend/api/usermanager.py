from typing import List, Dict, Tuple

import requests

from Player import Player


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
