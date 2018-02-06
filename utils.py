import os
import json
import requests
from __main__ import rawDataPath


season = 10  # should be defined later... globally somehow
last_season = 10  # must be int > 1


def createFolder():
    print("Creating folder ./data")
    os.mkdir(rawDataPath)


def isDownloaded(season):
    datapath = os.path.join(rawDataPath, "season_{}.json".format(season))
    if os.path.exists(datapath) == False:
        return False
    else:
        return True


def retrieveData(season):
    print("Downloading data from season {}".format(season))
    data = requests.get("https://www.lichess4545.com/api/get_season_games/?league=team4545&season={}".format(season))  # possibly include a safecheck here, should crash if season wrong?
    with open(os.path.join(rawDataPath, "season_{}.json".format(season)), "w") as f:
        json.dump(data.json(), f)


def checkData(seasons):  # this is the main function of this module!!
    if not os.path.exists(rawDataPath):
        createFolder()
        print("Created subdirectory {}".format(rawDataPath))
    for season in seasons:
        if not isDownloaded(season=season):
            retrieveData(season=season)
    print("All data downloaded!")
