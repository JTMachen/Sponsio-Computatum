# Import Required Libraries
import pandas as pd
from path import Path
import hashlib
from datetime import datetime
from Website import Place_Bet, secret, Calendar, basketball_win, hockey_win
import json
import pprint as pprint
import warnings
warnings.filterwarnings('ignore')
pptint = pprint.PrettyPrinter(indent=4)
from IPython.display import clear_output
import panel as pn
import getpass 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image 


# Create a Username and Password section for new users to input their new login information
special_characters = ['!','@','#','$','%','^','&','*','(',')']
numbers = ['1','2','3','4','5','6','7','8','9','0']
def new_user():
    # Print Sponsio Computatum logo
    img=mpimg.imread('Logo.png')
    imgplot = plt.imshow(img)
    imgplot.axes.get_xaxis().set_visible(False)
    imgplot.axes.get_yaxis().set_visible(False)
    plt.show(imgplot)
    # Open JSON file with every transaction
    with open('transaction_history.txt') as json_file:
        transaction_history = json.load(json_file)
    # Read user csv used to store user info
    csv_path = Path('user_info_dataframe.csv')
    user_info_dataframe = pd.read_csv(csv_path)
    user_info_dataframe.drop(columns = ['Unnamed: 0'],inplace=True)
    
    
    
    
    # Set count to limit the number of attempts that the user has to create a username
    attempts = 0
    while attempts < 5:
        # Ask for user's desired username
        username = input('Please input the username that you would like to use: ')
        # Verify that the selected username isn't being used by another user already
        if len(user_info_dataframe[user_info_dataframe['Username'] == username]) == 1:
            print('\nThe username that you have provided is already in use, please select another username.')
            attempts += 1
        else:
            attempts += 100
    # Once maximum number of attemtps is made without success, exit the function
    if attempts == 5:
        print('You have exceeded the maximum number of attempts. Please exit and try again. If you already have an account, plese type "Retuning User."')
        return
    
    
    
    
    # Ask for a password that is at least eight characters long
    # TODO: Check to ensure that the requirements are met
    print('\nYour password must be at least 8 characters long and contain at least one capital letter, one lowercase letter, one number, and one special character.')
    # Initialize a count to limit the number of attempts that the user has
    password_count = 0
    while password_count < 4:
        # Use getpass, which hides the password from the input text box
        password = getpass.getpass('\nPlease input the password that you would like to use: ')
        # Make sure that the password is long enough
        if len(password) < 8:
            print('Your password must be at least eight characters long. Please try again.')
            password_count += 1
        elif len(password) >= 8:
            # If input is correct length, ask for confirmation
            confirm_password = getpass.getpass('\nPlease reenter your password: ')
            # Convert password inputs to bytes
            confirm_password  = bytes(confirm_password, 'utf-8')
            password  = bytes(password, 'utf-8')
            # Check that both inputs are identical
            if confirm_password != password:
                print('\nThe passwords that you entered do not match.')
                password_count += 1
            elif confirm_password == password:
                # If passwords are acceptable, sha256 the password so that we're not saving actualy user passwords
                password = hashlib.sha256(password).hexdigest()
                password_count += 10
    # If max number of attempts is reached, exit the function
    if password_count == 4:
        print('You have exceeded the maximum number of attempts, please restart and try again.')
        return
    
    
    
    
    # Set count to limit number of attempts
    email_count = 0
    while email_count < 4:
        # Ask for an email and ensure that it at least contains an '@'
        user_email = input('\nPlease provide us with the email that you would like to be associated with this account: ')
        if '@' not in user_email:
            print('Please enter a valid email address.')
            email_count += 1
        # Check email not currently being used
        elif len(user_info_dataframe[user_info_dataframe['Email_Address'] == user_email]) >= 1:
            print('\nThe email address that you have provided is already in use, please use a different email address.')
            email_count += 1
        else:
            # Ask for confirmation
            confirm_user_email = input('\nPlease reenter your email address: ')
            # If they don't match, try again
            if confirm_user_email != user_email:
                print('\nThe email address that you entered does not match the original email that was provided. Please try again.')
            elif confirm_user_email == user_email:
                email_count += 10
    # Return if max attempts are reached
    if email_count == 4:
        print('You have exceeded the maximum number of attempts, please restart and try again.')
        return
    
    
    
    
    # Ask for an Ethereum wallet address
    address_count = 0
    while address_count < 4:
        # Ask the user for their public testnet address
        user_account_address = input('\nPlease enter your Ethereum Testnet public account address. If you do not wish to be included in the Ethereum Testnet server, please type in "no": ')
        if user_account_address == 'no' or user_account_address == 'No':
            address_count += 10
        # Make sure that the address provided is not already being used
        if len(user_info_dataframe[user_info_dataframe['User_Kovan_Testnet_Address'] == user_account_address]) >= 1:
            print('\nThe email address that you have provided is already in use, please use a different email address.')
            address_count += 1
        else:
            confirm_user_account_address = input('\nPlease reenter your Testnet public address: ')
            # If confirmation not equal to address provided, try again
            if confirm_user_account_address != user_account_address:
                print('\nThe Testnet address that you entered does not match the original email that was provided. Please try again.')
            elif confirm_user_account_address == user_account_address:
                address_count += 10
    # If max attempts reached, exit function
    if address_count == 4:
        print('You have exceeded the maximum number of attempts, please restart and try again.')
        return
    
    
    
    
    # Set a 'member since' column in dataframe
    member_since = datetime.now().strftime('%m-%d-%Y')
    # Append info to user info data frame
    user_info_dataframe = user_info_dataframe.append({'BetCoins':100, 'Username':username, 'Password':password, 'Email_Address': user_email, 'User_Kovan_Testnet_Address': user_account_address, 'Member_Since': member_since, 'Last_Login': datetime.now().strftime('%m-%d-%Y')} , ignore_index=True)
    # Update the csv
    user_info_dataframe.to_csv('user_info_dataframe.csv')
    # Update JSON file
    transaction_history['Transactions'].append({
        'Username':username,
        'Transaction_Type': 'Account_Initialization',
        'Transaction_Amount': 100,
        'Transaction_Time': datetime.now().strftime('%m-%d-%y'),
        '':''
    })
    # Save new JSON
    with open('transaction_history.txt','w') as outfile:
        json.dump(transaction_history, outfile)
        
        
        
def account_actions(user_index,check_user_info,user_info_dataframe,username,password):
    # Print SC logo
    img=mpimg.imread('Logo.png')
    imgplot = plt.imshow(img)
    imgplot.axes.get_xaxis().set_visible(False)
    imgplot.axes.get_yaxis().set_visible(False)
    plt.show(imgplot)
    
    with open('transaction_history.txt') as json_file:
        total_transaction_history = json.load(json_file)
        transaction_history = total_transaction_history['Transactions']
        transaction_count = 0
        for item in transaction_history:
            if item['Username'] == username and item['Transaction_Type'] == 'Placed_Bet' and item['Status'] == 'Unclaimed':
                if item['Sport'] == 'HOCKEY':
                    games = hockey_win.hockey_win(item['Transaction_Time'])
                    for row in games['Winner']:
                        if item['Team_Bet'] == row.upper():
                            user_info_dataframe['BetCoins'][user_index] = user_info_dataframe['BetCoins'][user_index] + (int(item['Transaction_Amount']) * 1.5)                            
                            user_info_dataframe.to_csv('user_info_dataframe.csv')
                            total_transaction_history['Transactions'][transaction_count]['Status'] = 'Claimed'
                    total_transaction_history['Transactions'][transaction_count]['Status'] = 'Claimed'
                elif item['Sport'] == 'BASKETBALL':
                    games = basketball_win.basketball_win(item['Transaction_Time'])
                    for row in games['Winner']:
                        if item['Team_Bet'] == row.upper():
                            user_info_dataframe['BetCoins'][user_index] = user_info_dataframe['BetCoins'][user_index] + (item['Transaction_Amount'] * 1.5)
                            addition = user_info_dataframe['BetCoins'][user_index] + (item['Transaction_Amount'] * 1.5)
                            user_info_dataframe.to_csv('user_info_dataframe.csv')
                            total_transaction_history['Transactions'][transaction_count]['Status'] = 'Claimed'
                            print(f'You have won {addition} for your bet on the {item['Team_Bet']}')
                    total_transaction_history['Transactions'][transaction_count]['Status'] = 'Claimed'    
            transaction_count += 1
    with open('transaction_history.txt','w') as outfile:
        json.dump(total_transaction_history, outfile)
    
    # Set clear_count for fun
    clear_count = 0
    # Set and initial action
    action = 'Initial'
    # Set user balance
    balance = int(user_info_dataframe['BetCoins'][user_index])
    # Set a list of actions that will exit the function
    exit_list = ['Exit','exit']
    # Set list of actions that will be printed for the user to choose from
    action_list = ['Balance     ','Place_Bet','History     ','Leaderboard','Clear_Output','Update_Account','Calendar    ','Exit']
    # Set a loop that will keep running unless the user wants to exit function
    while action != 'Exit' or action != 'exit':
        # Open user dataframe
        balance = int(user_info_dataframe['BetCoins'][user_index])
        csv_path = Path('user_info_dataframe.csv')
        user_info_dataframe = pd.read_csv(csv_path)
        user_info_dataframe.drop(columns = ['Unnamed: 0'],inplace=True)
        # Ask user for a command and provide a list of commands
        print('Please select the action that you wish to complete:')
        list_count = 0
        while list_count < len(action_list):
            try:
                print(action_list[list_count],'          ',action_list[list_count +1])
            except:
                print(action_list[list_count])
            list_count += 2
        action = input()
        print('\n')
        # Once user selects an action, check it with the options below
        # If user selects 'Balance' show them their curreny balance
        if action == 'Balance' or action == 'balance':
            balance = int(user_info_dataframe['BetCoins'][user_index])
            print(f"Your account balance is {balance} BetCoins.")
            print('You may also view your token balance in your Ethereum wallet.\n')
            
        # Batman/Cat (If you know, you know)
        elif action == 'secret' or action == 'Secret':
            clear_output()
            secret.secret()
        
        # If user selects 'Place_Bet' run that .py file
        elif action == 'Place_Bet' or action =='place_bet' or action == 'place bet' or action == 'Place Bet' or action == 'Place bet':
            new_balance = Place_Bet.place_bet(balance,check_user_info,user_index,user_info_dataframe)
            print(f"Your new account balance is {new_balance} BetCoins.")
            user_info_dataframe['BetCoins'][user_index] = new_balance
            user_info_dataframe.to_csv('user_info_dataframe.csv')
            
        # 'History' opens JSON file with every transaction
        elif action == 'History' or action == 'history':
            with open('transaction_history.txt') as json_file:
                transaction_history = json.load(json_file)
            pprint.pprint(transaction_history)
            print('')
        
        # 'Leaderboard' shows highest balances in user info dataframe
        elif action == 'Leaderboard' or action == 'leaderboard' or action == 'Leader Board' or action == 'leader board' or action == 'Leader board' or action == 'Leader' or action == 'leader':
            leaderboard = user_info_dataframe[['Username','BetCoins']]
            new_index = range(1,len(leaderboard) + 1)
            leaderboard['Standing'] = new_index
            leaderboard = leaderboard.set_index('Standing')
            leaderboard_show = leaderboard[0:9]
            if user_index > 10:
                leaderboard_show.append(leaderboard[user_index + 1])
            row_count = 1
            for row in leaderboard_show['BetCoins']:
                row = int(row) - 100
                leaderboard_show['BetCoins'][row_count] = row
                row_count += 1
            print(leaderboard_show)
            print('')
        
        # Shows games being played today without making user place a bet
        elif action == 'Calendar' or action == 'calendar':
            todays_games = Calendar.calendar()
        
        # Search balance of any username
        elif action == 'Search' or action == 'search' or action == 'Search User' or action == 'search user' or action == 'Search user' or action == 'Search_User' or action == 'Search_user' or action == 'search_user':
            search_attempt = 0
            while search_attempt < 4:
                search = input('Who are you looking for?\n')
                search_df = user_info_dataframe[user_info_dataframe['Username'] == search]
                if len(search_df) == 0:
                    print('Sorry, but that username is not in our system. Please try again.')
                    search_attempt += 1
                else:
                    print(search_df[['Username','BetCoins']])
                    search_attempt += 10
            if search_attempt == 4:
                print('You have reached the maximum number of attempts. Please try again.')
            
            
        # Clears screen except for action choices and logo
        elif action =='Clear_Output' or action == 'Clear_output' or action == 'clear_output' or action == 'Clear Output' or action == 'Clear output' or action == 'clear output' or action == 'Clear' or action == 'clear':
            clear_output()
            # If the user clears the screen more than 6 times, logo changes to an image of Mr Clean
            if clear_count > 5:
                img=mpimg.imread('MrClean.png',0)
            else:
                img=mpimg.imread('Logo.png')
            imgplot = plt.imshow(img)
            imgplot.axes.get_xaxis().set_visible(False)
            imgplot.axes.get_yaxis().set_visible(False)
            plt.show(imgplot)
            clear_count += 1
            
        # Allows user to update account information
        elif action == 'Update_Account' or action == 'update_account' or action == 'Update_account' or action == 'Update Account' or action == 'update account' or action == 'Update account':
            # Ask for password again
            confirm_password = getpass.getpass('Please enter your password: ')
            confirm_password  = bytes(confirm_password, 'utf-8')
            # Confirm passwords match
            if hashlib.sha256(confirm_password).hexdigest() == password:
                # Ask what they want to change
                account_action_list ['Username    ','Password','Email_Address','Testnet_Address']
                action_count = 0
                while action_count < len(account_action_list):
                    try:
                        print(account_action_list[action_count],'          ',account_action_list[action_count+1])
                    except:
                        print(account_action_list[action_count])
                    action_count += 2
                account_action = input('What would you like to update?')
                if account_action == 'Username' or account_action == 'uesrname':
                    new_username = input('Please select the new username that you wish to use: ')
                    check_new_username = user_info_dataframe[user_info_dataframe['Username'] == new_username]
                    if len(check_new_username) > 0:
                        print("We're sorry, but that username is already taken. Please try again.")
                    else:
                        user_info_dataframe['Username'][user_index] = new_username
                        print(f'Your username has been updated. Your new username is {new_username}')
                elif account_action == 'Password' or account_action == 'password':
                    new_password = getpass.getpass('Please enter your new password: ')
                    if hashlib.sha256(new_password).hexdigest() == password:
                        print('Sorry, but the password that you have chosen is already your current password.')
                    else:
                        confirm_new_password = getpass.getpass('Please reenter your new password: ')
                        if hashlib.sha256(confirm_new_password).hexdigest() == hashlib.sha256(new_password).hexdigest():
                            user_info_dataframe['Password'][user_index] = new_password
                            print('Your password has now been updated.')
                elif account_action == 'Email_Address' or account_action == 'Email_address' or account_address == 'email_address' or account_address == 'Email Address' or account_action == 'Email address' or account_action == 'email address' or account_action == 'email' or account_action == 'Email':
                    new_email == input('Please enter the new email that you want associated with your account: ')
                    if '@' not in new_email:
                        print('Please enter a valid email address.')
                    else:
                        user_info_dataframe['Email_Address'][user_index] = new_email
                elif account_action == 'Testnet_Address' or account_address == 'Testnet_address' or account_address == 'testnet_address' or account_address == 'Testnet Address' or account_action == 'Testnet address' or account_action == 'testnet address' or account_address == 'Testnet' or account_action == 'testnet':
                    new_kovan = input('Please enter the new Kovan address that you want associated with this account.')
                    user_info_dataframe['User_Kovan_Testnet_Address'][user_index] = new_kovan
                    print(f'Your Testnet Address has been updated. The new address is {new_kovan}')
                elif account_action not in exit_list:
                    print(f'{account_action} is not a valid command. Please try again.')
                else:
                    clear_output()
                    img=mpimg.imread('Logo.png')
                    imgplot = plt.imshow(img)
                    imgplot.axes.get_xaxis().set_visible(False)
                    imgplot.axes.get_yaxis().set_visible(False)
                    plt.show(imgplot)
                    
                    
        elif action not in exit_list:
            print(f'"{action}" is not a valid command. Please try again.')
        
        
        else:
            clear_output()
            img=mpimg.imread('Logo.png')
            imgplot = plt.imshow(img)
            imgplot.axes.get_xaxis().set_visible(False)
            imgplot.axes.get_yaxis().set_visible(False)
            plt.show(imgplot)
            print('Logging out of your account')
            return check_user_info
    return check_user_info


# If they have already created an account, ask them to login to their account
def returning_user():
    # Print SC logo
    img=mpimg.imread('Logo.png')
    imgplot = plt.imshow(img)
    imgplot.axes.get_xaxis().set_visible(False)
    imgplot.axes.get_yaxis().set_visible(False)
    plt.show(imgplot)
    # Read user info data frame
    csv_path = Path('user_info_dataframe.csv')
    user_info_dataframe = pd.read_csv(csv_path)
    user_info_dataframe.drop(columns = ['Unnamed: 0'],inplace=True)
    # Limit nuber of attempts
    attempts = 0
    while attempts < 4:
        # Ask for username
        username = input('Please enter your username: ')
        # Check that the username is in the data frame
        check_user_info = user_info_dataframe[user_info_dataframe['Username'] == username]
        if len(check_user_info) == 0:
            print('The username that you have entered does not exist. Please make sure that you have input the correct username or create a new account.')
            attempts += 1
        else:
            attempts += 10
    # Exit if max attempts is reached, exit function
    if attempts == 4:
        print('You have exceed the maximum number of attempts, please restart and try again.')
        return
    password_count = 0
    # select user info based on username
    user_index = check_user_info.index[0]
    while password_count < 4:
        password_count += 1
        password = getpass.getpass('Please input your password: ')
        password  = bytes(password, 'utf-8')
        password = hashlib.sha256(password).hexdigest()
        # Check provided password against password in data frame
        user_password = check_user_info['Password'][user_index]
        if user_password == password:
            password_count += 10
        elif user_password != password:
            print('\nThe password that you entered is incorrect.')
    # If max attempts reached, exit function
    if password_count == 4:
        print('You have exceeded the maximum number of attempts, please restart and try again.')
        return
    print('Loading Account...')
    # Clear output, update last login, and run 'account_actions' function
    user_info_dataframe['Last_Login'][user_index] = datetime.now().strftime('%m-%d-%Y')
    user_info_dataframe.to_csv('user_info_dataframe.csv')
    clear_output()
    new_balance = account_actions(user_index,check_user_info,user_info_dataframe,username,password)
    
# Function that provides initial user interface
def user_interface():
    # Clear output to start, then print SC logo
    clear_output()
    img=mpimg.imread('Logo.png')
    imgplot = plt.imshow(img)
    imgplot.axes.get_xaxis().set_visible(False)
    imgplot.axes.get_yaxis().set_visible(False)
    plt.show(imgplot)
    exit_list = ['Exit','exit']
    user = 'None'
    while user != 'Exit' or user != 'exit':
        # Ask the user if they are a new or returning user
        user = input('Are you a new or returning user?')
        # If they are a new user, run new_user function
        if user == 'new' or user == 'New' or user == 'New User' or user == 'New_User' or user == 'new user' or user == 'new_user' or user == 'New_user':
            clear_output()
            new_user()
        # If they are a returning user, run returning_user function
        elif user == 'returning' or user == 'Returning' or user == 'Retuning User' or user == 'returning user' or user == 'Returning_User' or user == 'Returning_user' or user == 'retuning_user' or user == 'return' or user == 'Return':
            clear_output()
            returning_user()
        # If input is not new, returning, or exit, inform user that the action is invalid
        elif user not in exit_list:
            print(f'{user} is not a valid command. Please try again.')
        # If the user wants to exit the program, exit the program
        else:
            clear_output()
            img=mpimg.imread('Logo.png')
            imgplot = plt.imshow(img)
            imgplot.axes.get_xaxis().set_visible(False)
            imgplot.axes.get_yaxis().set_visible(False)
            plt.show(imgplot)
            print('Thank you for visiting Sponsio Computatum.')
            break
