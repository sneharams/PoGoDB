from __future__ import print_function, unicode_literals
from inspect import currentframe, getframeinfo


import requests
import pprint
import sys
import time
import urllib
import pickle
# import urllib.request
from bs4 import BeautifulSoup
from db import Database


from PyInquirer import style_from_dict, Token, prompt, Separator
import inquirer
from inquirer.themes import GreenPassion
from pprint import pprint

objs_root = 'obj/'
contents_file = 'contents.'
contents = dict()

# def open_contents():
#     if

def save_obj(obj, name):
    with open('obj/' + name + '.pkl', 'sb') as f:
        pass
        #pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

print_toggle = False # set to True if you want error output
def print_error(flag, year, table):
    # if (print_toggle == True):
    #     print("ERROR:", flag)
    #     print("_year: ", year)
    #     print("_table:", table)
    #     print()
    pass

file_name = getframeinfo(currentframe()).filename

def flag(line_num, code_text, tag, flags):
    # for future if we want to add other tags
    if (print_toggle == True):
        print()
        print('\tFile "' + file_name + ', line ' + str(line_num))
        print('\t\t' + code_text)
        print('\t\t' + ' ' * (len(code_text)-1) + '^')
        print()

        bullet = ' > '
        print('[' + tag + ']' + bullet + flags[0])
        if (len(flags) > 1):
            indent = len(tag) + ' ' * 2
            for flag in flags[1:]:
                print(indent + bullet + flag)
        print()



#region EVENT BOX VARIABLES

root_url = 'https://gamepress.gg/pokemongo/legacy-special-box-list?page='
earliest_event = 'Winter 2016 Event Part 1'
table_identifier = 'Item Box Name'
# known malformed titles
bad_titles = {'April 200 Box 2': 2020 }
known_box_types = {
    'Event Box',
    'Special Box',
    'Ultra Box',
    'Adventure Box'
}

box_types = set()
item_types = set()
bar_scale = 100
num_pages = 19 # TODO: remove hardcoding

#endregion

#region UNOWN EVENT VARIABLES

unown_url = 'https://www.serebii.net/pokemongo/unownevents.shtml'
unown_variations = "ABCDEFGHIJKLMNOPQRSTUVWXYZ!?"
unown_event_count = [0] * len(unown_variations)

#endregion


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

# event boxes
def update_loading_bar(page, table, num_tables):
    # Calculate Completion Percent
    i_base = page/num_pages*bar_scale
    page_scale = bar_scale/num_pages
    i = int(i_base + (table+1)/num_tables*page_scale)
    # Update Progress Bar
    printProgressBar(i, bar_scale, prefix = 'Progress:', suffix = 'Complete', length = 50)

# unown events
def update_loading_bar(event_num, num_events):
    # Calculate Completion Percent
    i = (event_num+1)/num_events*100
    # Update Progress Bar
    printProgressBar(i, num_events, prefix = 'Progress:', suffix = 'Complete', length = 50)


def extract_unown_info():
    # Get HTML
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }
    request = urllib.request.Request(unown_url, headers=hdr)
    opener = urllib.request.build_opener()
    response = opener.open(request)
    response_bytes = response.read()
    response_text = response_bytes.decode("utf8")
    response.close()
    # Extract Data
    soup = BeautifulSoup(response_text, 'html.parser')
    table = soup.find('table', {'class':'dextable'}).find('tbody') # TODO: check periodically
    # Less straightforward, but for future use, being able to access more info would be useful
    headers = table.find('tr').find_all('td')
    i = 0
    # Get header containing letters
    for header in headers:
        if (header.text == 'Available Letters'):
            break
        i += 1
    events = table.find_all('tr')[1:]
    for event in events:
        td_text = event.find_all('td')[i].text

        word = '' # for future use?
        if '(' in td_text:
            # Sometimes letter info contains the word formed in parenthesis
            # Example: 'S, A, F, R, I (Safari)'
            text_parts = td_text.split('(')
            if (len(text_parts) > 2):
                line_num = getframeinfo(currentframe()).lineno - 1
                code_text = 'if (len(text_parts) > 2):' # way to not hardcode?
                flags = []
                tag = "Warning"
                flags.append("More then one '(' found in unown letters td text.")
                flags.append('Text: "' + td_text + '"')
                flag(159, code_text, tag, flags)
            word_part = text_parts[1]
            p_i = word_part.index(')')
            word = word_part[:p_i] # get the word
            td_text = text_parts[0]

        text_parts = td_text.split('(') # sometime word formed by letters is included

    

events = dict()

def extract_info():
    # extract data from legacy tables
    page_num = 0
    year = 'current'
    count = 0
    # print("Retrieving Database", end=' ')
    # sys.stdout.flush()  
    while (page_num < num_pages): # TODO: remove hardcoding 
        page_url = root_url + str(page_num)
        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        request = urllib.request.Request(page_url, headers=hdr)
        opener = urllib.request.build_opener()
        response = opener.open(request)
        # time.sleep(10)
        response_bytes = response.read()
        response_text = response_bytes.decode("utf8")
        response.close()
        # with urllib.urlopen(req) as response:
        soup = BeautifulSoup(response_text, 'html.parser')
        # print(soup)
        # TODO: check over time to see if structure of page changes (need to manually updated? or is there a better way?)
        # The first table on each page is an irrelevant one, so remove
        tables = soup.find_all('table')[1:]
        # if (page_num == 4):
        #     print(soup.find(id='node-284691').text)

        # The first relevant table on each page is the current event table, so remove after the first page
        if (page_num != num_pages):
            tables = tables[1:]
        page_count = 0
        for table in tables:
            # print(table.text)
            flags = []
            title = ''
            title_found = False
            if (year == 'current'):
                year = 2021 # TODO: update so that year changes don't need to be hardcoded
                events[year] = dict()
            else:
                # check for structural update errors
                try:
                    title = table.parent.parent.parent.find('div').find('div').text
                    title_found = True
                except:
                    flag = "Title not found for a table"
                    flags.append(flag)
                    print_error(flag, year, count)

                # extract year
                prefix = '20'
                if (prefix in title):
                    start = title.find(prefix)
                    end = start + 4
                    new_year = year
                    flags = []
                    try:
                        new_year = int(title[start:end])
                        # check for appropriate year change
                        if (new_year == year-1):
                            year = new_year
                            events[year] = dict()
                            count = 0
                        elif (new_year != year):
                            # check for known malformed titles
                            if (title in bad_titles):
                                year = bad_titles[title]
                            else:
                                flag = "Year doesn't make sense chronologically (Title: '" + title + "')"
                                print_error(flag, year, count)
                                flags.append(flag)
                    except:
                        # check for known malformed titles
                        if (title in bad_titles):
                            year = bad_titles[title]
                        else:
                            flag = "Failed parsing year"
                            print_error(flag, year, count)
                            flags.append(flag)

                # may indicate malformed title (title doesn't have a year) or wrong that an incorrect div was found (need to update structure on line 46)
                elif (title_found == True):
                    flag = "Title incorrect or doesn't have year"
                    print_error(flag, year, count)
                    flags.append(flag)

            try: 
                rows = table.find('tbody').find_all('tr')
            except:
                # for some reason tbody is removed in pages 4 and up
                row = table.find_all('tr')
            events[year][count] = {
                'event': title,
                'flags': flags
            }
            box_names = rows[0].find_all('th')
            for name in box_names[1:]:
                if (name.text not in known_box_types):
                    flag = "Box type isn't known (Type: " + name.text + ")"
                    print_error(flag, year, count)
                    flags.append(flag)
                    box_types.add(name.text)
                events[year][count][name.text] = dict()
            for row in rows[1:]:
                items = row.find_all('td')
                # print(items)
                item = row.find('th').text
                if item not in item_types:
                    item_types.add(item)
                if (len(items)==0):
                    # item box cost TODO
                    pass
                else:
                    box_col = 0
                    for name in box_names[1:]:
                        try:
                            events[year][count][name.text][item] = int(items[box_col].text)
                        except:
                            # print(items[box_col].text)
                            events[year][count][name.text][item] = 0
                        box_col += 1
            update_loading_bar(page_num, page_count, len(tables))
            page_count += 1
            count += 1

        page_num += 1

def fetch_item_chart(box, item):
    for year in events:
        # print('_________________________________________________')
        # print('| ' + str(year) + ' |', end="")
        print(str(year) + '\t')
        for count in events[year]:
            if box in events[year][count]:
                item_count = 0
                if item in events[year][count][box]:
                    item_count = events[year][count][box][item]
                if (item_count > 0):
                    whitespace = ''
                    if (count < 10):
                        whitespace = ' '
                    
                    print("\t[" + str(count) + "] " + whitespace + str(item_count))

def prompt_box_selection():
    misc_options = ['Quit']
    options = list(box_types) + misc_options
    question = [
        inquirer.List(
            'selection',
            message = 'Select Box',
            choices = options,
            default = 'Event Box'
        )
    ]
    answer = inquirer.prompt(question, theme=GreenPassion())['selection']
    return answer

def prompt_item_selection():
    options = list(item_types)
    for i in range(len(options)):
        if (options[i].startswith("#")):
            options[i] = options[i][5:] # where item name starts
    misc_options = ['Return to box selection', 'Quit']
    options += misc_options
    question = [
        inquirer.List(
            'selection',
            message = 'Select Item',
            choices = options
        )
    ]
    answer = inquirer.prompt(question, theme=GreenPassion())['selection']
    return answer

def prompt_new_comparison():
    options = ['Select a different box', 'Quit']
    question = [
        inquirer.List(
            'selection',
            message = 'Select Option',
            choices = options
        )
    ]
    answer = inquirer.prompt(question, theme=GreenPassion())['selection']
    return answer

def prompt_database():
    options = ['Event Boxes', 'Unown Count (Events)', 'Quit']
    question = [
        inquirer.List(
            'selection',
            message = 'Select Database',
            choices = options
        )
    ]
    answer = inquirer.prompt(question, theme=GreenPassion())['selection']
    # TODO: update hardcoding
    if (answer == options[0]): prompt_box_selection()
    elif (answer == options[1]): pass #prompt_unown()
    else: shutdown()

def shutdown():
    # if (database_updated):
    pass



if __name__ == '__main__':
    # while True:
    # print("Fetching Database...")
    # printProgressBar(0, bar_scale, prefix = 'Progress:', suffix = 'Complete', length = 50)
    # extract_info()
    # print()
    # print("What box would you like to compare?")
    # print()
    # while True:
    #     box = prompt_box_selection()
    #     if (box == 'Quit'):
    #         print("Have a nice day!")
    #         break
    #     else:
    #         item = prompt_item_selection()
    #         if (item == 'Quit'):
    #             print("Have a nice day!")
    #             break
    #         elif (item == 'Return to box selection'):
    #             continue
    #         else:
    #             if (item != 'Item Box Cost'):
    #                 item = "# of " + item
    #             fetch_item_chart(box, item)
    #             next_comparison = prompt_new_comparison()
    #             if (next_comparison == 'Select a different box'):
    #                 continue
    #             else:
    #                 break
    database = Database()



