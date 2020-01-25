# Import required libraries
from datetime import datetime
from path import Path
import pandas as pd
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen as Ureq
import json
import warnings
warnings.filterwarnings('ignore')



def hockey_win(date):
    url = 'https://www.hockey-reference.com/leagues/NHL_2020_games.html'
    # Run through BeautifulSoup steps
    uClient = Ureq(url)
    raw_content = uClient.read()
    page_soup = soup(raw_content, "html.parser")
    html = list(page_soup.children)[3]
    game = html.findAll(class_ = 'left')
    results = html.findAll(class_ = 'right')
    game = [team.get_text() for team in game]
    results = [team.get_text() for team in results]
    results_drop = ['LOG']
    results = [results for results in results if results not in results_drop]
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
    bin_len = 4
    start = 0
    end = start + bin_len
    week_list = []
    while end < (len(results) + 1):
        week = results[start:end]
        start = end
        end = start + bin_len
        week_list.append(week)
    df_1 = pd.DataFrame(week_list)
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
    df_1.columns = ['Visitor_Goals','Home_Goals','Attendance','Time']
    total_df = pd.concat([df,df_1],axis=1,join='inner')
    win_count = 0
    win_list = []
    while win_count < len(total_df):
        if (total_df['Visitor_Goals'][win_count]) > (total_df['Home_Goals'][win_count]):
            win_list.append(total_df['Visitor'][win_count])
        elif (total_df['Home_Goals'][win_count]) > (total_df['Visitor_Goals'][win_count]):
            win_list.append(total_df['Home'][win_count])
        elif (total_df['Home_Goals'][win_count]) != '' and (total_df['Visitor_Goals'][win_count]) != '' and (total_df['Home_Goals'][win_count]) == (total_df['Visitor_Goals'][win_count]):
            win_list.append('Tie')
        else:
            win_list.append('Incomplete') 
        win_count += 1
    total_df['Winner'] = win_list
    todays_games = total_df[total_df['Date'] == date]
    todays_games = todays_games.reset_index()
    return todays_games