# Import required libraries
from datetime import datetime
from path import Path
import pandas as pd
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen as Ureq
import json
import warnings
warnings.filterwarnings('ignore')
from IPython.display import clear_output


teams_list = ['ATL','BRK','BOS','CHO','CHI','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHO','POR','SAC','SAS','TOR','UTA','WAS']
teams_dict = {
    'Atlanta Hawks':'Hawks',
    'Brooklyn Nets':'Nets',
    'Boston Celtics':'Celtics',
    'Charlotte Hornets':'Hornets',
    'Chicago Bulls':'Bulls',
    'Cleveland Cavaliers':'Cavaliers',
    'Dallas Mavericks':'Mavericks',
    'Denver Nuggets':'Nuggets',
    'Detroit Pistons':'Pistons',
    'Golden State Warriors':'Warriors',
    'Houston Rockets':'Rockets',
    'Indiana Pacers':'Pacers',
    'Los Angeles Clippers':'Clippers',
    'Los Angeles Lakers':'Lakers',
    'Memphis Grizzlies':'Grizzlies',
    'Miami Heat':'Heat',
    'Milwaukee Bucks':'Bucks',
    'Minnesota Timberwolves':'Timberwolves',
    'New Orleans Pelicans':'Pelicans',
    'New York Knicks':'Knicks',
    'Oklahoma City Thunder':'Thunder',
    'Orlando Magic':'Magic',
    'Philadelphia 76ers':'76ers',
    'Phoenix Suns':'Suns',
    'Portland Trail Blazers':'Blazers',
    'Sacramento Kings':'Kings',
    'San Antonio Spurs':'Spurs',
    'Toronto Raptors':'Raptors',
    'Utah Jazz':'Jazz',
    'Washington Wizards':'Wizards',
    }

def basketball_bet():
    # Get the current month and day in order to get the games playing today
    current_month_text = datetime.now().strftime('%B').lower()
    current_day = datetime.now().strftime('%d')
    # Pull the url based on the current month
    try:
        url = 'https://www.basketball-reference.com/leagues/NBA_2020_games-' + current_month_text + '.html'
    except:
        print('There are currently no basketball games being played today')
        return
    uClient = Ureq(url)
    raw_content = uClient.read()
    page_soup = soup(raw_content, "html.parser")
    html = list(page_soup.children)[3]
    schedule_text = html.findAll(class_="left")
    # Get the text from the html
    schedule = [game.get_text() for game in schedule_text]
    # Fill dataframe with game date, visiting team name, and home team name
    bin_len = 3
    start = 0
    end = start + bin_len
    week_list = []
    while end < (len(schedule) + 1):
        week = schedule[start:end]
        start = end + 1
        end = start + bin_len
        week_list.append(week)
    df_1 = pd.DataFrame(week_list)
    df_1.columns = ['Date','Visitor','Home']
    # Clean all of the comlumns
    row_count = 0
    new = df_1['Date'].str.split(" ", n = 3, expand = True) 
    while row_count < len(df_1):
        df_1['Date'][row_count] = new[2][row_count][:-1]
        row_count += 1
    game_time = html.findAll(class_ = 'right')
    game_time = [team.get_text() for team in game_time]
    bin_len = 4
    start = 0
    end = start + bin_len
    week_list = []
    while end < (len(game_time) + 1):
        week = game_time[start:end]
        start = end
        end = start + bin_len
        week_list.append(week)
    df = pd.DataFrame(week_list)
    df.columns = ['Game_Time(EST)','Stat1','Stat2','Stat3']
    df = df['Game_Time(EST)']
    todays_games = pd.concat([df_1,df],axis = 1, join = 'inner')
    todays_games = todays_games[todays_games['Date'] == current_day]
    if len(todays_games) == 0:
        print('There are currently no basketball games being played today.')
        return
    todays_games = todays_games.reset_index()
    todays_games = todays_games[['Visitor','Home','Game_Time(EST)']]
    todays_games['Home'] = todays_games['Home'].apply(lambda x: teams_dict[x])
    todays_games['Visitor'] = todays_games['Visitor'].apply(lambda x: teams_dict[x])
    return todays_games