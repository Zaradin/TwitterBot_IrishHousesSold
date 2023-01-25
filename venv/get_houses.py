# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import time
import requests
import numpy as np
import ast
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import tweepy

class HouseData():

    def __init__(self, startMonth, Year):

        self.base_url = ""
        # day will always be 01 since we want the start of the month all the way to the end of the month which will be the first day of following month
        self.day = '01'

        # Start month
        self.startMonth = str(startMonth)
        #Year
        self.year = str(Year)
        # End month will always be the month after startMonth
        self.endMonth = str(int(startMonth)+1)
        # If getting data for the Month of December we need the ending date of 1st January, of the follwoing year
        self.endYear = str(int(Year)+1)

        # Use this for every month EXECPT DECEMBER
        self.full_Date = self.day + "/" + self.startMonth + "/" + self.year
        #End date
        self.end_Full_Date = self.day + "/" + self.endMonth + "/" + self.year
        # Use this for the month of DECEMBER end date

        self.dec_full_End_Date = self.day + "/" + "01" + "/" + self.endYear

        # Build the URL
        if(str(startMonth) == "12"):
            self.base_url = "https://www.propertypriceregister.ie/Website/npsra/PPR/npsra-ppr.nsf/PPR-By-Date&Start=1&Query=%5Bdt_execution_date%5D%3E=" + self.full_Date + "%20AND%20%5Bdt_execution_date%5D%3C0" + self.dec_full_End_Date + "&County=&Year=" + self.year + "&StartMonth=" + self.startMonth + "&EndMonth=" + "12" + "&Address="
            print(self.base_url)
        else:
            self.base_url = "https://www.propertypriceregister.ie/Website/npsra/PPR/npsra-ppr.nsf/PPR-By-Date&Start=1&Query=%5Bdt_execution_date%5D%3E=" + self.full_Date + "%20AND%20%5Bdt_execution_date%5D%3C0" + self.end_Full_Date + "&County=&Year=" + self.year + "&StartMonth=" + self.startMonth + "&EndMonth=" + self.endMonth + "&Address="

    # Returns a python 2D list of the house data
    # First arary index [1][] is the house index which contains the data for any paticular house
    # second array has three indexes  [1][0], [1][1], [1][2], first [1][0] one containing Sale date, second [1][1] has sale Price and [1][2] third has house address
    def getHouseData(self):
        self.responce = requests.get(self.base_url, verify=False)

        self.soup = BeautifulSoup(self.responce.text, 'html.parser')

        # Extract the javascript line that contains that data I want, data is in an array called 'dataSearchResults'
        self.raw_JS_Extracted = self.soup.find(text=re.compile('dataSearchResults'))

        # Extract the above specific line
        self.js_Line_Extracted = self.raw_JS_Extracted.splitlines()[2]

        # Remove the first 24 & last chars from the string as it's only javascript code, Only want the 2D array object [ [] ]
        self.extractedLine_toList = self.js_Line_Extracted[24:-1]

        # convert this 2D array into a python readble list
        # First arary index [1][] is the house index which contains the data for paticular house
        # second array has three indexes  [1][0], [1][1], [1][2], first [1][0] one containing Sale date, second [1][1] has sale Price and [1][2] third house address
        self.housePriceList = ast.literal_eval(self.extractedLine_toList)


        return self.housePriceList

houses = HouseData("03", "2022")
d = houses.getHouseData()

np.savetxt('houses.txt', d, fmt='%s')
