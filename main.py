#!/usr/bin/env python

"""Summary: Main file which contains an interactive tool."""
from config import *
from utils import update, seasonValid
from models import *
from plot import plot


def interactive():
    """Allows for interaction via command line"""
    while True:
        try:
            season = int(raw_input("Input the season up to which you wish to generate a report: "))
            if season <= 0:
                print("Please enter a positive integer, try again...")
            else:
                if seasonValid(season):
                    break
                else:
                    print("The season you selected does not exist yet, select a smaller number...")
        except ValueError:
            print("This is not a whole number, try again...")

    seasons = range(1, season + 1)

    print("Checking if all data is already downloaded...")
    update(seasons=seasons)

    print("Now generating plots...")
    plot(finalSeason=season)


if __name__ == "__main__":
    interactive()
