# Import required libraries
from datetime import datetime
from path import Path
import pandas as pd
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen as Ureq
import warnings
warnings.filterwarnings('ignore')


# Set dictionary and list to convert given team abbrvs to more readable names
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
    # Set the current date in a readable form and the form used for the html
    todays_date = datetime.now().strftime('%m-%d-%Y')
    date_html = datetime.now().strftime('%Y%m%d')
    # Set Opening Day date
    openeing_day = "03-26-2020"
    # Parse OD date
    OD = datetime.strptime(openeing_day, "%m-%d-%Y")
    # Set current date
    present = datetime.now()
    # If it is before OD, return from function
    if present.date() < OP.date():
        print('Opening Day is not until March 26. Please come back then.')
        return
    # Set url for todays date if season has already started
    url = 'https://www.espn.com/mlb/schedule/_/date/' + date_html
    # Make sure that there are acutally games being played
    # If there are not, the url will not work
    try:
        uClient = Ureq(url)
        raw_content = uClient.read()
    except:
        print('There are no games being played on this day.')
        return
    # Run through BeautifulSoup steps to pull out desired data
    page_soup = soup(raw_content, "html.parser")
    html = list(page_soup.children)[3]
    game = html.findAll(class_ = 'external')
    game_date_list = []
    # Fix dates given into readable datetime format
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
    # Get the names of the teams that are playing on that day
    game = html.findAll(class_ = 'team-name')
    game = [team.get_text() for team in game]
    game_list = []
    for item in game:
        # The abbrvs are only the last three characters in the str
        item = item[-3:]
        game_list.append(item)
    # Split home and away teams from the list of cleaned teams
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
    # Apply the lambda function that will clean the team names into more colloquial names
    todays_games['Home'] = todays_games['Home'].apply(lambda x: teams_dict[x])
    todays_games['Visitor'] = todays_games['Visitor'].apply(lambda x: teams_dict[x])
    # return data frame of games that are being played today
    return todays_games