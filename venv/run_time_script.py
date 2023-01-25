import random

import schedule
import time
from datetime import *
import os
import calendar
import numpy

import get_houses

#schedule.every().friday.at("18:30").do(getThisWeeksHouses())

def getThisWeeksHouses():
    month = datetime.datetime.now().strftime("%m")
    year = str(datetime.datetime.today().year)

    houses = get_houses.HouseData(month, year)
    houseData = houses.getHouseData()

    ThreeHouseToTweet = random.choices(houseData, k=3)

    constructTweet(ThreeHouseToTweet)

def constructTweet():
    tweet = ""

    day = calendar.day_name[date.today().weekday()]


constructTweet()

