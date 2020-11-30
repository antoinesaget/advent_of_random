import argparse
import random
import pickle
import traceback
import sys
import os
import datetime as dt
from pathlib import Path

def createArgParser():
    arg_parser = argparse.ArgumentParser(description='Advent of Random (AoR) is an additional challenge to Advent of Code that pick a random programming language for you everyday !')
    arg_parser.add_argument('-u', '--username', type=str, help='change your username')
    arg_parser.add_argument('-a', '--add', type=str, help='add a new langage to the list')
    arg_parser.add_argument('-r', '--remove', type=str, help='add a new langage to the list')
    arg_parser.add_argument('-l', '--list', action='store_true', help='show the list of possible languages')
    arg_parser.add_argument('--reset', action='store_true', help='remove persistent datas')
    return arg_parser

def init(filename):
    # Get user inputs
    username = input('Please choose a username:\n\t')
    print(f'Welcome to Advent of Random {username}!')
    languages = input('What languages do you want me to pick from ? (comma separated)\n\t')
    languages = languages.split(',')
    languages = [language.strip() for language in languages]
    languages = list(filter(None, languages))

    # Save the user preference in a file
    data = {
        'languages' : languages,
        'bag' : languages.copy(),
        'username' : username 
    }
    update_persistent_data(filename, data)
    
    # Inform the user
    print('--------------------------') 
    print('Setup successfully finished with the following languages:') 
    print('\t' + ', '.join(languages))
    print('--------------------------') 
    print('Launch the script once a day to know your language for the day ;)\nGood luck!')
    sys.exit(0)

# Pick a language from the data bag
def pick(data):
    # If the bag is empty, fill it
    if not data['bag']:
        data['bag'] = data['languages'].copy()
    
    # Pop a random language from the bag
    bag = data['bag']
    random.shuffle(bag)
    return bag.pop()

# Read persistent data from the savefile filename
def get_persistent_data(filename):
    try:
        f = open(filename, 'rb')
        pass
    except IOError:
        traceback.print_exc()
        sys.exit(-1)
    data = pickle.load(f)
    f.close()
    return data

# Write persistent data from the savefile filename
def update_persistent_data(filename, data):
    try:
        f = open(filename, 'wb')
        pass
    except IOError:
        traceback.print_exc()
        sys.exit(-1)
    
    pickle.dump(data, f)
    f.close()

# return false if at least one argument was provided by the user
def handle_args(args, filename, data):
    cont = True

    # Update the username
    if args.username:
        data['username'] = args.username
        print(f'Username successfully updated: {args.username}')
        cont = False
    
    # Add a new language
    if args.add:
        if args.add in data['languages']:
            print(f'The {args.add} language is already listed!')
        else:
            data['languages'].append(args.add)
            data['bag'].append(args.add)
            print(f'The {args.add} language has been successfully added!')
        cont = False
    
    # remove a language
    if args.remove:
        if args.remove in data['languages']:
            data['languages'].remove(args.remove)
            if args.remove in data['bag']:
                data['bag'].remove(args.remove)
                

            print(f'The {args.remove} language has been successfully removed!')
        else:
            print(f'The {args.remove} language is not in the list!')
        cont = False

    # List programming laguages (the bag stays hidden from the user however ;))
    if args.list:
        print(', '.join(data['languages']))    
        cont = False

    # Remove the savefile
    if args.reset:
        if os.path.exists(filename):
            os.remove(filename)
            print('Persistent datas successfully removed!')
        else:
            print('No persistent data to remove.')
        sys.exit(0)
    
    return cont


def get_part_of_day(hour):
    return (
        'morning' if 4 <= hour <= 11
        else
        'afternoon' if 12 <= hour <= 17
        else
        'evening' if 18 <= hour <= 22
        else
        'night'
    )

def format_line_in_snowflake(lines):
    # The longest line
    n = len(max(lines, key=len))
    
    # Center lines by adding ' ' before and after
    for i in range(len(lines)):
        remaining_spaces = n - len(lines[i])
        a = int(remaining_spaces / 2)
        b = a + (remaining_spaces % 2)
        lines[i] = " " * a + lines[i] + " " * b

    empty_line = " " * n

    # Bad code for upper and lower lines
    a = int((n + 4 + 19)/ 8)
    b = (n + 4 + 19) % 8
    line = ".:*~*:._" * int(a / 2) + "_" * int(a % 2 + b + 1) + ".:*~*:._" * int(a / 2 - 1) + ".:*~*:."
    
    
    msg = f"""
{line}
.   {empty_line}                  .
.   {empty_line}      .      .    .
.   {empty_line}      _\/  \/_    .
.   {lines[0]  }       _\/\/_     .
.   {lines[1]  }   _\_\_\/\/_/_/_ .
.   {lines[2]  }    / /_/\/\_\ \  .
.   {lines[3]  }       _/\/\_     .
.   {empty_line}       /\  /\     .
.   {empty_line}      '      '    .
.   {empty_line}                  .
{line}
    """
    # Ascii art from https://asciiart.website/

def pretty_print(data, language):
    part_of_day = get_part_of_day(dt.datetime.today().hour)
    lines = [
    f"Good {part_of_day} {data['username']}!",
    f"I hope you are ready for today's challenge!",
    f"Today, you'll have to programm in... {language}!",
    f"Good luck!"
    ]

    msg = format_line_in_snowflake(lines) # A nice addition would be to have other ascii arts and pick a random one ! ;)
    print(msg)

if __name__ == "__main__":
    filename = '.AoR_save.pk'
    args = createArgParser().parse_args()

    # If there is no savefile, initialize it
    if not Path(filename).is_file():
        init(filename)
    
    # Load data from the savefile
    data = get_persistent_data(filename)

    cont = handle_args(args, filename, data)

    # Pick a language only if the user hasn't given any argument
    if cont:
        todays_language = pick(data)
        pretty_print(data, todays_language)

    # Update data to the savefile
    update_persistent_data(filename, data)