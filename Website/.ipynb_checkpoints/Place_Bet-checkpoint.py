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
from Website import baseball_bet,basketball_bet,hockey_bet,football_bet



def place_bet(balance,check_user_info,user_index,user_info_dataframe):
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
    # Ask for the user's team input
    try:
        len(todays_games)
    except:
        return
    if len(todays_games) == 0:
        print('There are no games being played today.\n')
        return
    print(todays_games)
    team = input('\nPlease type in the team that you would like to bet on: ')
    # Check to ensure that the team is playing today
    row_count = 0
    while row_count < (len(todays_games)+1):
        if todays_games['Visitor'][row_count] == team or todays_games['Home'][row_count] == team or todays_games['Home'][row_count].lower() == team or todays_games['Visitor'][row_count].lower() == team:
            row_count += 1000
        else:
            row_count += 1
    if row_count == (len(todays_games)+1):
        print('The team that you have selected either does not exist or is not playing today.')
        return
    bet_number = 0
    while bet_number < 4:
        bet_number += 1
        bet_amount = (input(f'\nHow many BetCoins would you like to bet on the {team.upper()} to win the game today?'))
        try:
            bet_amount = int(bet_amount)
        except:
            print('Please input a whole number.')
            bet_number += 1
        if bet_amount < 0:
            print('You cannot bet negative money. Try again Slick.')
            bet_number += 1
        elif bet_amount > balance:
            print('You do not currently have enough BetCoins to place this bet. Please lower your bet.\n')
            bet_number += 1
        else:
            bet_number += 10
    if bet_number == 4:
        print('You have exceeded the maximum number of attempts to place a bet. Please log back into your account to place another bet.')
        return
    verification = input(f'\nAre you sure you would like to bet {bet_amount} BetCoins on the {team} to win? Please type yes or no.')
    if verification == 'y' or verification == 'yes' or verification == 'Y' or verification == 'Yes':
        new_balance = balance - bet_amount
        user_info_dataframe['BetCoins'][user_index] = new_balance
        csv_path = Path('user_info_dataframe.csv')
        user_info_dataframe.to_csv(csv_path)
        transaction_history['Transactions'].append({
            'Username':check_user_info['Username'][user_index],
            'Transaction_Type': 'Placed_Bet',
            'Transaction_Amount': bet_amount,
            'Transaction_Time': datetime.now().strftime('%m-%d-%y'),
            'Team_Bet': team.upper(),
            'Sport':sport.upper(),
            '':''
        })
        with open('transaction_history.txt','w') as outfile:
            json.dump(transaction_history, outfile)
        print('Thank you, your bet has been placed. Please check back tomorrow to see if you won.\n')
    else:
        new_balance = balance
        print('Thank you, your bet has been cancelled.')
    return new_balance