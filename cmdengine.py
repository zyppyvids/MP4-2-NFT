# This file is used to access the console
from datetime import datetime
import os

log_file = open('log.txt','a')

def start_log():
    '''A function that prints to the console the current date and time in the format "2017-12-29 11:24:48.042720"'''
    now = datetime.now()

    print(f"--- {str(now)} ---")
    log_file.write(f"--- {str(now)} ---" + os.linesep)

def log(input_text, show_tag = True):
    '''A function that prints to the console in the format [<current_time>] <input_text> / <input_text>'''
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    
    if show_tag:
        input_text =  f"[{current_time}] {input_text}" 
    
    print(input_text)
    log_file.write(input_text + os.linesep)


def get_input(input_text, show_tag = True):
    '''A function used by the program to get user input.'''
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    if show_tag:
        input_text =  f"[{current_time}] {input_text}" 

    return input(input_text)