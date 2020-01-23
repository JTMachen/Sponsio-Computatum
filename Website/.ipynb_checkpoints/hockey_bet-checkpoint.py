# Import required libraries
from datetime import datetime
from path import Path
import pandas as pd
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen as Ureq
import json
import warnings
warnings.filterwarnings('ignore')


def hockey_bet():
    # Pull in url for schedule
    # TODO: Check date, and if it is not during the season, exit function
    url = 'https://www.hockey-reference.com/leagues/NHL_2020_games.html'
    # Run through BeautifulSoup steps
    uClient = Ureq(url)
    raw_content = uClient.read()
    page_soup = soup(raw_content, "html.parser")
    html = list(page_soup.children)[3]
    game = html.findAll(class_ = 'left')
    game = [team.get_text() for team in game]
    drop_list = ['Date','Visitor','Home','Notes','']
    # Clean data
    game = [game for game in game if game not in drop_list]
    bin_len = 3
    start = 0
    end = start + bin_len
    week_list = []
    while end < (len(game) + 1):
        week = game[start:end]
        start = end
        end = start + bin_len
        week_list.append(week)
    df = pd.DataFrame(week_list)
    df.columns = ['Date','Visitor','Home']
    # Clean team names into readable format
    row_count = 0
    visitor = df['Visitor'].str.split(" ", expand = True) 
    home = df['Home'].str.split(" ", expand = True) 
    while row_count < len(df):
        if visitor[2][row_count] == None:
            df['Visitor'][row_count] = visitor[1][row_count]
        elif visitor[2][row_count] != None:
            df['Visitor'][row_count] = visitor[2][row_count]
        if home[2][row_count] == None:
            df['Home'][row_count] = home[1][row_count]
        elif home[2][row_count] != None:
            df['Home'][row_count] = home[2][row_count]
        row_count += 1
    # Only select todays games
    todays_date = datetime.now().strftime('%Y-%m-%d')
    todays_games = df[df['Date'] == todays_date]
    todays_games = todays_games.reset_index()
    todays_games = todays_games[['Visitor','Home']]
    return todays_games