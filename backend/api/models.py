from . import db 

class Summoner(db.Model):
    player_id = db.Column(db.String(100), primary_key=True)
    summoner_name = db.Column(db.String(20))
    region = db.Column(db.String(10))
    