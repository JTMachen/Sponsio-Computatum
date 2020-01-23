# Import required libraries
from datetime import datetime
from path import Path
import pandas as pd
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen as Ureq
import warnings
warnings.filterwarnings('ignore')

teams_list = ['ATL','BAL','BOS','ARI','CHC','CLE','TEX',' KC','DET','CHW','HOU','WSH','TOR','LAA','LAD','MIA','MIL','MIN','NYY','NYM','OAK','COL','PHI',' TB',' SD','PIT','CIN','STL','SEA',' SF']
teams_dict = {
    'ATL':'Braves',
    'BAL':'Orioles',
    'BOS':'Red Sox',
    'ARI':'Diamond Backs',
    'CHC':'Cubs',
    'CLE':'Indians',
    'TEX':'Rangers',
    ' KC':'Royals',
    'DET':'Tigers',
    'CHW':'White Sox',
    'HOU':'Astros',
    'WSH':'Nationals',
    'TOR':'Blue Jays',
    'LAA':'Angels',
    'LAD':'Dodgers',
    'MIA':'Marlins',
    'MIL':'Brewers',
    'MIN':'Twins',
    'NYY':'Yankees',
    'NYM':'Mets',
    'OAK':'Athletics',
    'COL':'Rockies',
    'PHI':'Phillies',
    ' TB':'Rays',
    ' SD':'Padres',
    'PIT':'Pirates',
    'CIN':'Reds',
    'STL':'Cardinals',
    'SEA':'Mariners',
    ' SF':'Giants',
    }



def baseball_bet():
    todays_date = datetime.now().strftime('%m-%d-%Y')
    date_html = datetime.now().strftime('%Y%m%d')
    string_input_with_date = "03-26-2020"
    past = datetime.strptime(string_input_with_date, "%m-%d-%Y")
    present = datetime.now()
    if present.date() < past.date():
        print('Opening Day is not until March 26. Please come back then.')
        return
    date_count = 0
    url = 'https://www.espn.com/mlb/schedule/_/date/' + date_html
    try:
        uClient = Ureq(url)
        raw_content = uClient.read()
    except:
        print('There are no games being played on this day.')
        return
    page_soup = soup(raw_content, "html.parser")
    html = list(page_soup.children)[3]
    game = html.findAll(class_ = 'external')
    game_date_list = []
    for x in range(1,len(game)):
        game_date = game[x]['href'].split('/')[5].split('-')[-3:-1]
        game_date.append('2020')
        sent_str = ""
        for i in game_date:
            sent_str += str(i) + "-"
        sent_str = sent_str[:-1]
        date = datetime.strptime(sent_str, '%m-%d-%Y')
        date = date.strftime('%m-%d-%Y')
        game_date_list.append(date)
    game = html.findAll(class_ = 'team-name')
    game = [team.get_text() for team in game]
    game_list = []
    for item in game:
        item = item[-3:]
        game_list.append(item)
    bin_len = 2
    start = 0
    end = start + bin_len
    week_list = []
    while end < (len(game_list) + 1):
        week = game_list[start:end]
        start = end
        end = start + bin_len
        week_list.append(week)
    df = pd.DataFrame(week_list)
    df.columns = ['Visitor','Home']
    df['Date'] = game_date_list
    todays_games = df[df['Date'] == todays_date]
    todays_games['Home'] = todays_games['Home'].apply(lambda x: teams_dict[x])
    todays_games['Visitor'] = todays_games['Visitor'].apply(lambda x: teams_dict[x])
    return todays_games