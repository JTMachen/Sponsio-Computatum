import pandas as pd
from path import Path
import hashlib
from datetime import datetime
import json
import pprint as pprint
import warnings
warnings.filterwarnings('ignore')
pptint = pprint.PrettyPrinter(indent=4)
from IPython.display import clear_output
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from IPython.display import Image


def secret():
    secret_attempts = 0
    while secret_attempts < 1000:
        secret_action = input()
        if secret_action == 'Batman':
            clear_output()
            attempts = 0
            image = Image(filename="./BATMAN.gif.png")
            display(image)
            while attempts < 1000:
                exit = input()
                if exit == 'Exit' or exit == 'exit':
                    clear_output()
                    return
                else:
                    clear_output()
                    display(image)
                    attempts += 1
            secret_attempts += 1
        elif secret_action == 'Cat':
            attempts = 0
            image = Image(filename="./Cat.png")
            display(image)
            while attempts < 1000:
                exit = input()
                if exit == 'Exit' or exit == 'exit':
                    clear_output()
                    return
                else:
                    clear_output()
                    display(image)
                    attempts += 1
            secret_attempts += 1
        elif secret_action == 'exit' or secret_action == 'Exit':
            clear_output()
            return
        else:
            secret_attempts += 1