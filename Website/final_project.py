# Import Required Libraries
import pandas as pd
from path import Path
import hashlib
from datetime import datetime
from Website import Place_Bet
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
from Website import secret


# Create a Username and Password section for new users to input their new login information
special_characters = ['!','@','#','$','%','^','&','*','(',')']
numbers = ['1','2','3','4','5','6','7','8','9','0']
def new_user():
    img=mpimg.imread('Logo.png')
    imgplot = plt.imshow(img)
    imgplot.axes.get_xaxis().set_visible(False)
    imgplot.axes.get_yaxis().set_visible(False)
    plt.show(imgplot)
    with open('transaction_history.txt') as json_file:
        transaction_history = json.load(json_file)
    csv_path = Path('user_info_dataframe.csv')
    user_info_dataframe = pd.read_csv(csv_path)
    user_info_dataframe.drop(columns = ['Unnamed: 0'],inplace=True)
    
    
    
    
    
    attempts = 0
    while attempts < 5:
        username = input('Please input the username that you would like to use: ')
        if len(user_info_dataframe[user_info_dataframe['Username'] == username]) == 1:
            print('\nThe username that you have provided is already in use, please select another username.')
            attempts += 1
        else:
            attempts += 100
    if attempts == 5:
        print('You have exceeded the maximum number of attempts. Please exit and try again. If you already have an account, plese type "Retuning User."')
        return
    
    
    
    
    
    print('\nYour password must be at least 8 characters long and contain at least one capital letter, one lowercase letter, one number, and one special character.')
    password_count = 0
    while password_count < 4:
        password = getpass.getpass('\nPlease input the password that you would like to use: ')
        if len(password) < 8:
            print('Your password must be at least eight characters long. Please try again.')
            password_count += 1
        elif len(password) >= 8:
            confirm_password = getpass.getpass('\nPlease reenter your password: ')
            confirm_password  = bytes(confirm_password, 'utf-8')
            password  = bytes(password, 'utf-8')
            if confirm_password != password:
                print('\nThe passwords that you entered do not match.')
                password_count += 1
            elif confirm_password == password:
                password = hashlib.sha256(password).hexdigest()
                password_count += 10
    if password_count == 4:
        print('You have exceeded the maximum number of attempts, please restart and try again.')
        return
    
    
    
    
    
    email_count = 0
    while email_count < 4:
        user_email = input('\nPlease provide us with the email that you would like to be associated with this account: ')
        if '@' not in user_email:
            print('Please enter a valid email address.')
            email_count += 1
        elif len(user_info_dataframe[user_info_dataframe['Email_Address'] == user_email]) >= 1:
            print('\nThe email address that you have provided is already in use, please use a different email address.')
            email_count += 1
        else:
            confirm_user_email = input('\nPlease reenter your email address: ')
            if confirm_user_email != user_email:
                print('\nThe email address that you entered does not match the original email that was provided. Please try again.')
            elif confirm_user_email == user_email:
                email_count += 10
    if email_count == 4:
        print('You have exceeded the maximum number of attempts, please restart and try again.')
        return
    
    
    
    
    
    address_count = 0
    while address_count < 4:
        user_account_address = input('\nPlease enter your Kovan Testnet public account address. If you do not have a Kovan Testnet account, please get one and try again: ')
        if len(user_info_dataframe[user_info_dataframe['Email_Address'] == user_email]) >= 1:
            print('\nThe email address that you have provided is already in use, please use a different email address.')
            address_count += 1
        else:
            confirm_user_account_address = input('\nPlease reenter your Kovan address: ')
            if confirm_user_account_address != user_account_address:
                print('\nThe Kovan address that you entered does not match the original email that was provided. Please try again.')
            elif confirm_user_account_address == user_account_address:
                address_count += 10
    if address_count == 4:
        print('You have exceeded the maximum number of attempts, please restart and try again.')
        return
    
    
    
    
    
    member_since = datetime.now().strftime('%m-%d-%Y')
    user_info_dataframe = user_info_dataframe.append({'BetCoins':100, 'Username':username, 'Password':password, 'Email_Address': user_email, 'User_Kovan_Testnet_Address': user_account_address, 'Member_Since': member_since} , ignore_index=True)
    user_info_dataframe.to_csv('user_info_dataframe.csv')
    transaction_history['Transactions'].append({
        'Username':username,
        'Transaction_Type': 'Account_Initialization',
        'Transaction_Amount': 100,
        'Transaction_Time': datetime.now().strftime('%m-%d-%y'),
        '':''
    })

    with open('transaction_history.txt','w') as outfile:
        json.dump(transaction_history, outfile)
        
        
        
def account_actions(user_index,check_user_info,user_info_dataframe,username,password):
    img=mpimg.imread('Logo.png')
    imgplot = plt.imshow(img)
    imgplot.axes.get_xaxis().set_visible(False)
    imgplot.axes.get_yaxis().set_visible(False)
    plt.show(imgplot)
    
    clear_count = 0
    action = 'Initial'
    balance = int(check_user_info['BetCoins'][user_index])
    exit_list = ['Exit','exit']
    action_list = ['Balance     ','Place_Bet','History     ','Leaderboard','Clear_Output','Update_Account','Exit']
    while action != 'Exit' or action != 'exit':
        csv_path = Path('user_info_dataframe.csv')
        user_info_dataframe = pd.read_csv(csv_path)
        user_info_dataframe.drop(columns = ['Unnamed: 0'],inplace=True)
        print('Please select the action that you wish to complete:')
        list_count = 0
        while list_count < len(action_list):
            try:
                print(action_list[list_count],'          ',action_list[list_count +1])
            except:
                print(action_list[list_count])
            list_count += 2
        action = input()
        if action == 'Balance' or action == 'balance':
            balance = int(check_user_info['BetCoins'][user_index])
            print(f"Your account balance is {balance} BetCoins.")
            print('You may also view your account balance in your Ethereum wallet.\n')
            
        elif action == 'secret' or action == 'Secret':
            clear_output()
            secret.secret()
        
        elif action == 'Place_Bet' or action =='place_bet' or action == 'place bet' or action == 'Place Bet' or action == 'Place bet':
            new_balance = Place_Bet.place_bet(balance,check_user_info,user_index,user_info_dataframe)
            check_user_info['BetCoins'][user_index] = new_balance
            
            
        elif action == 'History' or action == 'history':
            with open('transaction_history.txt') as json_file:
                transaction_history = json.load(json_file)
            pprint.pprint(transaction_history)
            print('')
        
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
        
        elif action =='Clear_Output' or action == 'Clear_output' or action == 'clear_output' or action == 'Clear Output' or action == 'Clear output' or action == 'clear output' or action == 'Clear' or action == 'clear':
            clear_output()
            if clear_count > 5:
                img=mpimg.imread('MrClean.png',0)
            else:
                img=mpimg.imread('Logo.png')
            imgplot = plt.imshow(img)
            imgplot.axes.get_xaxis().set_visible(False)
            imgplot.axes.get_yaxis().set_visible(False)
            plt.show(imgplot)
            clear_count += 1
            
        elif action == 'Update_Account' or action == 'update_account' or action == 'Update_account' or action == 'Update Account' or action == 'update account' or action == 'Update account':
            confirm_password = getpass.getpass('Please enter your password: ')
            confirm_password  = bytes(confirm_password, 'utf-8')
            if hashlib.sha256(confirm_password).hexdigest() == password:
                account_action = input('What would you like to update? Username, Password, Email_Address, or Kovan_Address? ')
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
                elif account_action == 'Kovan_Address' or account_address == 'Kovan_address' or account_address == 'kovan_address' or account_address == 'Kovan Address' or account_action == 'Kovan address' or account_action == 'kovan address' or account_address == 'Kova' or account_action == 'kovan':
                    new_kovan = input('Please enter the new Kovan address that you want associated with this account.')
                    user_info_dataframe['User_Kovan_Testnet_Address'][user_index] = new_kovan
                    print(f'Your Kovan Address has been updated. The new address is {new_kovan}')
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
    img=mpimg.imread('Logo.png')
    imgplot = plt.imshow(img)
    imgplot.axes.get_xaxis().set_visible(False)
    imgplot.axes.get_yaxis().set_visible(False)
    plt.show(imgplot)
    csv_path = Path('user_info_dataframe.csv')
    user_info_dataframe = pd.read_csv(csv_path)
    user_info_dataframe.drop(columns = ['Unnamed: 0'],inplace=True)
    attempts = 0
    while attempts < 4:
        username = input('Please enter your username: ')
        check_user_info = user_info_dataframe[user_info_dataframe['Username'] == username]
        if len(check_user_info) == 0:
            print('The username that you have entered does not exist. Please make sure that you have input the correct username or create a new account.')
            attempts += 1
        else:
            attempts += 10
    if attempts == 4:
        print('You have exceed the maximum number of attempts, please restart and try again.')
        return
    password_count = 0
    user_index = check_user_info.index[0]
    while password_count < 4:
        password_count += 1
        password = getpass.getpass('Please input your password: ')
        password  = bytes(password, 'utf-8')
        password = hashlib.sha256(password).hexdigest()
        user_password = check_user_info['Password'][user_index]
        if user_password == password:
            password_count += 10
        elif user_password != password:
            print('\nThe passwords that you entered is incorrect.')
    if password_count == 4:
        print('You have exceeded the maximum number of attempts, please restart and try again.')
        return
    print('Loading Account...')
    clear_output()
    new_balance = account_actions(user_index,check_user_info,user_info_dataframe,username,password)
    
def user_interface():
    clear_output()
    img=mpimg.imread('Logo.png')
    imgplot = plt.imshow(img)
    imgplot.axes.get_xaxis().set_visible(False)
    imgplot.axes.get_yaxis().set_visible(False)
    plt.show(imgplot)
    exit_list = ['Exit','exit']
    user = 'None'
    while user != 'Exit' or user != 'exit':
        user = input('Are you a new or returning user?')
        if user == 'new' or user == 'New' or user == 'New User' or user == 'New_User' or user == 'new user' or user == 'new_user' or user == 'New_user':
            clear_output()
            new_user()
        elif user == 'returning' or user == 'Returning' or user == 'Retuning User' or user == 'returning user' or user == 'Returning_User' or user == 'Returning_user' or user == 'retuning_user' or user == 'return' or user == 'Return':
            clear_output()
            returning_user()
        elif user not in exit_list:
            print(f'{user} is not a valid command. Please try again.')
        else:
            print('Thank you for visiting Sponsio Computatum.')
            break
