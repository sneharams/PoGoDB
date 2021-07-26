

from logger import log
from inspect import currentframe, getframeinfo

FILENAME = getframeinfo(currentframe()).filename


class Bundle:

    #region Later
    # Count
    count = None
    prev_count = None
    next_count = None

    # Price
    price = None
    prev_price = None
    next_price = None

    # Value
    value = None
    prev_value = None
    next_value = None

    # Date
    date = None
    prev_date = None
    next_date = None

    box = None
    event_name = None
    #endregion
    
    attributes = dict()

    def __init__(self, name, count, price, date, flag=False):
        """
        Initialize Bundle Item
        @params:
            pc      - Required  : previous bundle item - quantity of item in bundle
            pp      - Required  : previous bundle item - price of bundle
            pv      - Required  : previous bundle item - value of bundle item
            pd      - Required  : previous bundle item - date of bundle event
            nc      - Required  : next bundle item - quantity of item in bundle
            np      - Required  : next bundle item - price of bundle
            nv      - Required  : next bundle item - value of bundle item
            nd      - Required  : next bundle item - date of bundle event
        """
        self.name = name
        self.attributes['count'] = count
        self.attributes['price'] = price
        self.attributes['date'] = date
        self.attributes['name'] = name
        # value = count/price
        self.attributes['value'] = 0 #value
        # logs = []
        # logs.append('Count: ' + str(count))
        # logs.append('Price: ' + str(price))
        # logs.append('Value: ' + str(self.attributes['value']))
        # logs.append('Date: ' + str(date))
        # code = 'def __init__(self, name, count, price, date, flag=False):'
        if (flag):
            # log(file_name, 38, 'Item Add', logs, code)
            pass


    def get(self, key):
        return self.attributes[key]


    #region Setters

    def set_prev_count(bundle_item):
        """
        Set previous bundle item node for count
        @params:
            bundle      - Required  : bundle item to link (BundleItem)
        """
        prev_ = bundle_item

    def set_prev_price(bundle_item):
        """
        Set previous bundle item node for price
        @params:
            bundle      - Required  : bundle item to link (BundleItem)
        """
        prev_price = bundle_item

    def set_prev_value(bundle_item):
        """
        Set previous bundle item node for value
        @params:
            bundle      - Required  : bundle item to link (BundleItem)
        """
        prev_value = bundle_item

    def set_prev_date(bundle_item):
        """
        Set previous bundle item node for date
        @params:
            bundle      - Required  : bundle item to link (BundleItem)
        """
        prev_date = bundle_item

    def set_next_count(bundle_item):
        """
        Set next bundle item node for count
        @params:
            bundle      - Required  : bundle item to link (BundleItem)
        """
        prev_count = bundle_item

    def set_next_price(bundle_item):
        """
        Set next bundle item node for price
        @params:
            bundle      - Required  : bundle item to link (BundleItem)
        """
        prev_price = bundle_item

    def set_next_value(bundle_item):
        """
        Set next bundle item node for value
        @params:
            bundle      - Required  : bundle item to link (BundleItem)
        """
        prev_value = bundle_item

    def set_next_date(bundle_item):
        """
        Set next bundle item node for date
        @params:
            bundle      - Required  : bundle item to link (BundleItem)
        """
        prev_date = bundle_item

    #endregion

class Item:

    name = ''

    lists = {
        'price': [],
        'count': [],
        'value': [],
        'date': []
    }

    def __init__(self, name):
        self.name = name

    def add_bundle(self, bundle):
        # print(self.name, bundle.name)
        # print(bundle.name, bundle.get('date'), bundle.get('count'))
        for key in self.lists:
            if (len(self.lists[key]) == 0):
                self.lists[key].append(bundle)
                # print('hi')
                continue
            i_l = 0
            i_r = len(self.lists[key])
            i_prev = None
            i = len(self.lists[key])//2
            found = False
            while i != i_prev:
                l = self.lists[key][i]
                # logs = []
                # logs.append(l.get('name'))
                # code = 'l = self.lists[key][i]'
                # log(FILENAME, 169, 'Left Bundle', logs, code)
                if (l.get(key) <= bundle.get(key)): 
                    # print(1)
                    # print(l.get(key), bundle.get(key))
                    if (l.get('date') < bundle.get('date')):
                        # print(2)
                        if (i + 1 > len(self.lists[key])):
                            # print(3)
                            self.lists[key].append(bundle)
                            found = True
                            break
                        else:
                            # print(4)
                            r = self.lists[key][i+1]
                            if (r.get(key) > bundle.get(key)):
                                # print(5)
                                self.lists[key].insert(i+1, bundle)
                                found = True
                                break
                            else:
                                # print(6)
                                if (r.get('date') > bundle.get('date')):
                                    # print(7)
                                    self.lists[key].insert(i+1, bundle)
                                    found = True
                                    break
                                else:
                                    # print(8)
                                    i_prev = i
                                    i_l = i
                                    i = (i_l + i_r)//2
                                    continue
                    if (l.get('date') == bundle.get('date')):
                        pass
                        # print('rip', l.name, bundle.name)
                i_prev = i
                i_r = i
                i = (i_l + i_r)//2
            # print('date', bundle.get('date'))
            if (found != True):
                # print('ye')
                self.lists[key].insert(0, bundle)

 


class Items:
    
    items = dict()

    def __init__(self):
        pass

    def add(self, name, price, count, date, flag = False):
        # bundle = Bundle(name, count, price, date)
        # pprint(bundle.attributes)
        # print(count)
        # print(name)
        if name not in self.items:
            self.items[name] = Item(name)
        bundle = Bundle(name, count, price, date, flag)
        self.items[name].add_bundle(bundle)
        # logs = []
        # logs.append('Name: ' + bundle.get('name'))
        # logs.append('Count: ' + str(bundle.get('count')))
        # code = 'def add(self, name, price, count, date, flag = False):'
        # log(FILENAME, 226, 'After Check', logs, code)
        
        # print('yello', len(self.items[name].lists['price']))