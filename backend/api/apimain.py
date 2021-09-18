import os

from dotenv import load_dotenv
import backend.api.usermanager

APIKEY = os.getenv('APIKEY')


def run_api(summoner_name: str, region: str):
    load_dotenv()

    pid = backend.get_player_id(summoner_name, region, APIKEY)

    matches = backend.get_recent_matches(pid, region, APIKEY)