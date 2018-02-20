"""Summary: Contains useful functions"""
from config import *
import os
import json
import requests
from models import *

db = SqliteDatabase(dbname)


def seasonValid(season):
    request = requests.get("https://www.lichess4545.com/api/get_season_games/?league=team4545&season={}".format(season))
    # print json.load(data)
    if request.json()["games"]:
        return True
    else:
        return False


def createFolder(path):
    print("Creating folder ./{}".format(path))
    os.mkdir(path)


def isDownloaded(season):
    """Check if season (int) has been downloaded already"""
    datapath = os.path.join(rawDataPath, "season_{}.json".format(season))
    if os.path.exists(datapath) == False:
        return False
    else:
        return True


def retrieveData(season):
    """Request data from lichess4545 api and store it (.json) in rawDataPath"""
    print("Downloading data from season {}".format(season))
    data = requests.get("https://www.lichess4545.com/api/get_season_games/?league=team4545&season={}".format(season))  # possibly include a safecheck here, should crash if season wrong?
    with open(os.path.join(rawDataPath, "season_{}.json".format(season)), "w") as f:
        json.dump(data.json(), f)


def raw2db():
    """Finds all raw .jsons and inputs them to the database"""
    jsonPaths = sorted([os.path.join(rawDataPath, file) for file in os.listdir(rawDataPath) if file.endswith(".json")])  # sort to ensure season ids match season numbers
    for path in jsonPaths:
        print("Currently handling {}".format(path))
        with open(path, "r") as f:
            r = json.load(f)
        json2db(r)
    print("Finished unpacking all seasons...")


def json2db(jsonData):
    """Processes a .json and inputs it to the database"""
    games = jsonData["games"]
    season = int([int(s) for s in games[0]["season"].split() if s.isdigit()][0])
    Season.get_or_create(number=season)

    print("Unpacking players and games...")
    for game in games:
        # create player rows
        white_player, _ = Player.get_or_create(username=game["white"])
        black_player, _ = Player.get_or_create(username=game["black"])
        try:
            white_player.seasons.add(season)
        except:
            pass
        try:
            black_player.seasons.add(season)
        except:
            pass

        # create game row
        Game.get_or_create(
            white=white_player.id,
            black=black_player.id,
            link=game["game_id"],
            result=game["result"],
            white_username=game["white"],
            black_username=game["black"],
            season=season,
            white_team=game["white_team"],
            black_team=game["black_team"])


def update(seasons):  # this is the main function of this module!!
    """Updates the DB with all the raw data"""
    if not os.path.exists(path=dbname):
        db.create_tables([Season, Game, Player, Season.players.get_through_model()])
        print("Created a database...")
    # check if all data in DB already, then skip ahead
    if Game.select().where(Game.season == max(seasons)).exists():
        print 'Database already up to date...'
        pass
    else:
        for season in seasons:
            if not isDownloaded(season=season):
                retrieveData(season=season)
        print("All data downloaded...")
        raw2db()
        print("Entered raw data into db...")
