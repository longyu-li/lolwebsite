from typing import List

import usermanager
from . import db 
from Player import Player
from .models import Summoner

APIKEY = "RGAPI-ae2f07aa-f9a7-4f42-be10-7d4e08ba925a"
regions = {"na1": "americas", "br1": "americas", "la1": "americas", "la2": "americas", "jp1": "asia",
           "kr": "asia", "oc1": "americas", "eun1": "europe", "euw1": "europe", "ru": "europe", "tr1": "europe"}


def run_api(summoner_name: str, region: str) -> List[Player]:
    load_dotenv()
    
    pid = Summoner.query.filter_by(summoner_name='summoner_name').first().player_id
    if (pid is None) :
        pid = usermanager.get_player_id(summoner_name, region, APIKEY)
        new_summoner = Summoner(player_id=pid, summoner_name=summoner_name, region=region)
        db.session.add(new_summoner)
        db.session.commit    

    return pid    
    
"""

    matches = usermanager.get_recent_matches(pid, regions[region], 10, APIKEY)
    recent_players = list(filter(lambda x: x.get_total_games_played() > 1,
                                 usermanager.get_recent_players(pid, matches, regions[region], APIKEY).values()))
    recent_players.sort(reverse=True, key=lambda player: player.get_total_games_played())
    return recent_players


if __name__ == "__main__":
    # run_api("Minez", "na1")
    players = run_api("Minez", "na1")
    for p in players:
        print("{} played {} games together with you for a total of {} minutes in the last 10 games."
              "You have a {}% win rate together and {} has a {}% win rate against you."
              .format(p.summoner_name, p.get_total_games_played(), p.get_hours_played(), p.get_winrate_on_team(),
                      p.summoner_name, p.get_winrate_on_enemy()))
"""
