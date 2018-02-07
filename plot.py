from peewee import *
from config import *
from models import *
from queries import findSeasons, findPlayers, findNewPlayers
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


xaxis = [0 for i in range(1, 11)]
y1 = [len(findPlayers(season)) for season in range(1, 11)]
y2 = [len(findNewPlayers(season)) for season in range(1, 11)]
x = range(1, 11)

plt.plot(x, y1, label="Returning players")
plt.plot(x, y2, label="New players")
plt.fill_between(x, 0, y2, facecolor="green")
plt.fill_between(x, y1, y2, facecolor="blue")
plt.xlim(xmin=1, xmax=10)


plt.title("lichess4545")
plt.xlabel("Season")
plt.ylabel("Number of players")
plt.legend(loc=0)
plt.show()
