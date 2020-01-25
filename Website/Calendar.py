from Website import baseball_bet,basketball_bet,hockey_bet,football_bet
from datetime import datetime
from path import Path
import pandas as pd
import json
import warnings
warnings.filterwarnings('ignore')
from IPython.display import clear_output



def calendar():
    with open('transaction_history.txt') as json_file:
            transaction_history = json.load(json_file)
    sport_list = ['Basketball','Baseball','Football  ','Hockey']
    print('Please select the sport you would like:')
    list_count = 0
    while list_count < len(sport_list):
        try: 
            print(sport_list[list_count],'          ',sport_list[list_count+1])
        except:
            print(sport_list[list_count])
        list_count += 2
    sport = input()
    if sport == 'Basketball' or sport == 'basketball':
        todays_games = basketball_bet.basketball_bet()
    elif sport == 'Baseball' or sport == 'baseball':
        todays_games = baseball_bet.baseball_bet()
    elif sport == 'Hockey' or sport == 'hockey':
        todays_games = hockey_bet.hockey_bet()
    elif sport == 'Football' or sport == 'football':
        todays_games = football_bet.football_bet()
    else:
        print("You have entered a sport that is not currently in our system. Please try again. If you are looking for a specific sport, please email us at Sponsio_Computatum@gmail.com and we'll see what we can do. Thank you.")
    try:
        len(todays_games)
    except:
        print('There are no games being played today.\n')
        return
    if len(todays_games) == 0:
        print('There are no games being played today.\n')
        return
    print(todays_games)
    print('\n')