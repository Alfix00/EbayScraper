from bs4 import BeautifulSoup
from requests import get

########################################################################
url = 'https://www.ebay.it/sch/i.html?'
searchItem = "&_nkw="
spaceWord = "%20"
categoryID = "&_sacat="
pageNumber =  "_pgn="
itemsPerPage = "&_ipg=" #Items Per Page (200,100,50,25,10,5)
auctions = "&LH_Auction=1"
bin = "&LH_BIN=1"
classADS = "&LH_CAds=1"
freeShipping = "&LH_FS=1"
timeLeftMin = "&_sop=1"
timeLeftMax = "&_sop=10" #New Item
timeLeftAvg = "&_sop=12" #Best Result
priceLowerFirst = "&_sop=2"
priceHighestFirst = "&_sop=3"
priceAndShippingLowest = "&_sop=15"
priceAndShippingHighest = "&_sop=16"
newItem = "&LH_ItemCondition=11"
usedItem = "&LH_ItemCondition=12"
unknItemStatus = "&LH_ItemCondition=10"
#########################################################################

class Item:

    search_title = ""
    title = ""
    price = ""
    shipping_p = ""
    photo = ""
    time_left = ""
    bids = ""
    info = ""
    link = ""

    def __init__(self, title, price):
        title = title.replace("Nuova inserzione", "")   #Replace the  world
        self.title = title
        self.price = price
        self.search_title = ""
        self.shipping_p = ""
        self.photo = ""
        self.time_left = ""
        self.bids = ""
        self.info = ""
        self.link = ""

    def set_search_title(self, search_title):
        self.search_title = search_title

    def set_title(self, title):
        self.title = title

    def set_link(self,link):
        self.link = link

    def set_price(self, price):
        self.price = price

    def set_shipping_p(self, shipping_p):
        self.shipping_p = shipping_p

    def set_photo(self, photo):
        self.photo = photo

    def set_bids(self, bids):
        self.bids = bids

    def set_info(self, info):
        self.info = info

    def set_time_left(self, time_left):
        self.time_left = time_left

    def print_item(self):
        print(self.title)
        print(self.price)
        print(self.time_left)
        print(self.shipping_p)
        print(self.bids)
        print(self.info)
        print(self.link)

 #item = v1.get_search_history().__getitem__(1)
#print(item)

class Vault:

    search_history = [str]
    items = [[Item]]
    favourite = [str]

    def check_string (self, link):
        if isinstance(link, str):
            return True
        return False

    def add_channel_history(self, link):
        link = str(link)
        if self.check_string(link):
            self.search_history.append(link)

    def add_items (self, items):
        if isinstance(items, Item):
            self.items = self.items.append(items)

    def add_favourite (self, link):
        link = str(link)
        if self.check_string(link):
            self.items.append(link)

    def get_search_history(self):
        return self.search_history

    
    def get_items(self):
        return self.items


    def get_favourites(self):
        return self.favourite


    def get_index(self, string_list, index):
        item = str
        if isinstance(string_list, str) and isinstance(index, int):
            item = string_list.__getitem__(index)
        return item


###########################################################################################
def url_maker_0(vault):
    global url
    item_name = str(input("Digit the item you wanna search: "))
    item_name = item_name.replace(" ", spaceWord)
    url = url+searchItem+item_name+auctions+timeLeftMin
    print(url)
    if isinstance(vault, Vault):
        connect_1(vault, item_name)


def connect_1(vault, item_name):
    items = [Item]
    response = get(url)
    src = response.content
    html_soup = BeautifulSoup(src, 'html.parser')
    items = scrape_info_2(html_soup, item_name)
    vault.add_channel_history(url)
    vault.add_items(items)
    check = vault.get_items()
    itm_vault = vault.get_items()[0]
    for itm_vault in items:
        if isinstance(itm_vault, Item):
            itm_vault.print_item()



def scrape_info_2(html_soup, item_name):
    items = [Item]
    titles = html_soup.find_all("h3", class_="s-item__title")
    prices = html_soup.find_all(class_="s-item__price")
    shipping_p = html_soup.find_all(class_="s-item__shipping s-item__logisticsCost")
    time_left = html_soup.find_all(class_="s-item__time-left")
    bids = html_soup.find_all(class_="s-item__bids s-item__bidCount")
    info = html_soup.find_all(class_="SECONDARY_INFO")
    link = html_soup.find_all('a', {'class': 's-item__link'})
    ###################################################################################
    i = len(titles)
    index = 0

    while i > 0 and titles.__getitem__(index) and prices.__getitem__(index):
        try:
            item = Item(titles.__getitem__(index).text, prices.__getitem__(index).text)
            item.set_search_title(item_name)

            if link.__getitem__(index):
                item.set_link(link.__getitem__(index)['href'])
            if time_left.__getitem__(index):
                item.set_time_left(time_left.__getitem__(index).text)
            if shipping_p.__getitem__(index):
                item.set_shipping_p(shipping_p.__getitem__(index).text)
            if bids.__getitem__(index):
                item.set_bids(bids.__getitem__(index).text)
            if info.__getitem__(index):
                item.set_info(info.__getitem__(index).text)
        except:
            pass

        items.append(item)
        i = i - 1
        index = index + 1
    return items



###########################################################################################

def start():
    vault = Vault()
    url_maker_0(vault)


start()
