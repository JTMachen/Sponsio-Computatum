from datetime import datetime
from path import Path
import pandas as pd
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen as Ureq
import warnings
warnings.filterwarnings('ignore')


def football_bet():
    # Ensure that the football season is currently going on
    year_date = datetime.now().strftime('%Y-%m-%d')
    if year_date > 'February 2 2020' and year_date < 'September 10 2020':
        print("The next football season hasn't begun yet. Please come back on September 10.")
        return
    elif year_date < 'February 2 2020':
        url = 'https://www.pro-football-reference.com/years/2019/games.htm'
    else:
        url = 'https://www.pro-football-reference.com/years/2020/games.htm'
    # Run through BeautifulSoup steps to pull wanted data
    uClient = Ureq(url)
    raw_content = uClient.read()
    page_soup = soup(raw_content, "html.parser")
    html = list(page_soup.children)[3]
    teams_win_loss = html.findAll(class_ = 'left')
    game = html.findAll(class_ = 'right')
    game = [team.get_text() for team in game]
    teams_win_loss = [team.get_text() for team in teams_win_loss]
    removal = ['Day']
    teams_win_loss = [item for item in teams_win_loss if item not in removal]
    # Set todays date that will be used to select todays games
    date = datetime.now().strftime('%B %d')
    # Clean stats
    bin_len = 8
    start = 0
    end = start + bin_len
    week_list = []
    while end < (len(game) + 1):
        week = game[start:end]
        start = end + 1
        end = start + bin_len
        week_list.append(week)
    df_1 = pd.DataFrame(week_list)
    df_1.columns = ['Game_Week','Time (EST)','Stat1','Stat2','Stat3','Stat4','Stat5','Stat6']

    bin_len = 4
    start = 0
    end = start + bin_len
    week_list = []
    while end < (len(teams_win_loss) + 1):
        week = teams_win_loss[start:end]
        start = end
        end = start + bin_len
        week_list.append(week)
    df_2 = pd.DataFrame(week_list)
    df_2.columns = ['Day_Of_Week','Date','Home','Visitor']
    # Concat data frames
    football = pd.concat([df_1[['Game_Week','Time (EST)']],df_2[['Date','Home','Visitor']]],axis = 1,join = 'inner')
    # Select only games being played today
    todays_games = football[football['Date'] == date]
    # Return dataframe
    return todays_games