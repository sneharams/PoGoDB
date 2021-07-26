import pickle
import sys
import os.path
import urllib
from bs4 import BeautifulSoup
from pprint import pprint

sys.path.append(".")

from shopitem import Items 
from logger import log
from inspect import currentframe, getframeinfo

FILENAME = getframeinfo(currentframe()).filename






class Database:

    root = 'obj/'
    catalog_file = 'catalog.pkl'
    catalog = None

    # databases_loaders = {
    #     'Event Boxes': init_eventboxes
    # }

    boxes = dict()

    '''
        Boxes:
            time_
    '''

    item = {
        'boxes': dict(),
        'count': dict(),
        'value': dict(),
        'price': dict(),
    }

    items = Items()

    #region Database Loading Methods

    def print_loading_bar (self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        """
        Call in a loop to create terminal progress bar.
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
    def update_paged_loading_bar(self, page, num_pages, item, num_items):
        """
        Calculate and update loading bar for paginated web sources.
        @params:
            page        - Required  : current page (Int)
            item        - Required  : current item (Int)
            num_pages   - Required  : # of pages (Int)
            num_items   - Required  : # of items on page (Int)   
        """
        # Calculate Completion Percent
        base_percent = page/num_pages*100
        page_percent = 100/num_pages
        i = int(base_percent + (item+1)/num_items*page_percent)
        # Update Progress Bar
        self.print_loading_bar(i, 100, prefix = 'Progress:', suffix = 'Complete', length = 50)



    def get_soup(self, url):
        """
        Get souped html of a webpage.
        @params:
            url     - Required  : url of webpage (Str)
        """
        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        request = urllib.request.Request(url, headers=hdr)
        opener = urllib.request.build_opener()
        response = opener.open(request)
        response_bytes = response.read()
        response_text = response_bytes.decode("utf8")
        response.close()
        soup = BeautifulSoup(response_text, 'html.parser')
        return soup



    def load_event_boxes(self):
        url = 'https://gamepress.gg/pokemongo/legacy-special-box-list?page='
        
        # known info
        bad_titles = {'April 200 Box 2': 2020 }
        known_box_types = {
            'Event Box',
            'Special Box',
            'Ultra Box',
            'Adventure Box'
        }

        box_types = set()
        item_types = set()
        num_pages = 2 # TODO: remove hardcoding

        # extract data from legacy tables
        page_num = 0
        year = 'current'
        count = 0
        # print("Retrieving Database", end=' ')
        # sys.stdout.flush()  
        while (page_num < num_pages): # TODO: remove hardcoding 
            page_url = url + str(page_num)
            soup = self.get_soup(page_url)
            # TODO: check over time to see if structure of page changes (need to manually updated? or is there a better way?)
            # The first table on each page is an irrelevant one, so remove
            tables = soup.find_all('table')[1:]

            # The first relevant table on each page is the current event table, so remove after the first page
            if (page_num != num_pages):
                tables = tables[1:]
            page_count = 0
            tab = -1
            for table in tables:
                tab += 1
                # print(table.text)
                flags = []
                title = ''
                title_found = False
                if (year == 'current'):
                    year = 2021 # TODO: update so that year changes don't need to be hardcoded
                    self.boxes[year] = dict()
                else:
                    # check for structural update errors
                    try:
                        title = table.parent.parent.parent.find('div').find('div').text
                        title_found = True
                    except:
                        flag = "Title not found for a table"
                        # flags.append(flag)
                        # print_error(flag, year, count)

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
                                self.boxes[year] = dict()
                                # count = 0
                            elif (new_year != year):
                                # check for known malformed titles
                                if (title in bad_titles):
                                    year = bad_titles[title]
                                else:
                                    flag = "Year doesn't make sense chronologically (Title: '" + title + "')"
                                    # print_error(flag, year, count)
                                    # flags.append(flag)
                        except:
                            # check for known malformed titles
                            if (title in bad_titles):
                                year = bad_titles[title]
                            else:
                                flag = "Failed parsing year"
                                # print_error(flag, year, count)
                                flags.append(flag)

                    # may indicate malformed title (title doesn't have a year) or wrong that an incorrect div was found (need to update structure on line 46)
                    elif (title_found == True):
                        flag = "Title incorrect or doesn't have year"
                        # print_error(flag, year, count)
                        flags.append(flag)

                try: 
                    rows = table.find('tbody').find_all('tr')
                except:
                    # for some reason tbody is removed in pages 4 and up
                    row = table.find_all('tr')
                # events[year][count] = {
                #     'event': title,

                #     'flags': flags
                # }
                box_names = rows[0].find_all('th')
                for name in box_names[1:]:
                    if (name.text not in known_box_types):
                        flag = "Box type isn't known (Type: " + name.text + ")"
                        # print_error(flag, year, count)
                        # flags.append(flag)
                        # box_types.add(name.text)
                    # events[year][count][name.text] = dict()
                for row in rows[1:]:
                    items = row.find_all('td')
                    # print(items)
                    item = row.find('th').text
                    # if item not in item_types:
                    #     item_types.add(item)
                    if (len(items)==0):
                        # item box cost TODO
                        pass
                    else:
                        box_col = 0
                        for name in box_names[1:]:
                            # print(name)
                            flag = False
                            # DEBUG
                            if (page_num == num_pages-1 and tab == 4 and box_col == 3):
                                logs = []
                                logs.append('Box:   ' + name.text)
                                logs.append('Count: ' + str(count))
                                logs.append('Item:  ' + item)
                                code = 'if (page_num == num_pages-1 and tab == 3 and box_col == 3):'
                                log(FILENAME, 230, 'Last Items', logs, code)
                            # DEBUG
                            if (name.text == 'Adventure Box' and item == '# of Super Incubators'):
                                flag = True
                            try:
                                # print(int(items[box_col].text))
                                # events[year][count][name.text][item] = int(items[box_col].text)
                                self.items.add(item[:], 0, int(items[box_col].text), count, flag)
                                
                            except Exception as e:
                                self.items.add(item[:], 0, 0, count, flag)
                                # print(items[box_col].text)
                                # events[year][count][name.text][item] = 0
                                # self.items.add(item, 0, int(items[box_col].text), 0)
                                pass
                            box_col += 1
                # self.update_paged_loading_bar(page_num, num_pages, page_count, len(tables))
                page_count += 1
                count += 1

            page_num += 1

    #endregion

    def __init__(self):
        if (os.path.isfile(self.root + self.catalog_file)):
            catalog = self.load_obj(self.catalog_file)
        else:
            self.load_event_boxes()
            print(self.items.items)

            '''
            JOSHUAAAAA READ THIS

            so this code creates 'bundles'
                - a bundle is a specific instance of the item being sold
            these bundles get sorted into lists of different types for each 'item'
                - an item (it's a type) holds all the bundles of that type sorted in these lists
            there is also an 'items' type that holds all the 'item' objects

            so in the code below i'm printing out all of the pokeball bundles
                - it's printing the:
                    - date (it's not actually a date, just the number of the box which increases the earlier it is)
                    - count (the number of that item type in the bundle)
            
            the code isn't right and it keeps printing the same values
            no matter what item name and list i request, all the bundles print 9 and 16

            # what i found out
            the values printed are from the last bundle created (i logged the last items for u)
                - i think it's a super incubator with the count of 16
                - 9 is the earliest box date

            in the 'add_bundle' method in Item, when i print the name value for the left bundle it's comparing to,
                it keeps printing the same name for all the items, so it's messed up already 
                (and I'm assuming the sorting isn't working because the right bundle option is never reached)
                - the 'add_bundle' method sorts the created bundle into the lists
                - the 'add' method in 'Items' creates the bundle and calls 'add_bundle'

            '''
            for nitem in self.items.items['# of Pokeballs'].lists['count']:
                print(nitem.get('date'), nitem.get('count'))
            # pprint(self.items.items['# of Incense'].lists)
    
    def load_obj(self, name):
        with open(self.root + name + '.pkl', 'rb') as f:
            return pickle.load(f)

    def save_obj(self, name):
        with open('obj/' + name + '.pkl', 'sb') as f:
            pass
            #pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

