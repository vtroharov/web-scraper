from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time, json, re, requests, sys, time
from datetime import datetime
import tkinter as tk


def get_magic_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=magic&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data['magic']['usd']

def get_anima_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=anima&vs_currencies=usdt"
    response = requests.get(url)
    data = response.json()
    print(data)
    return data['anima']['usd']

def save_realm_data():
    url = 'https://app.treasure.lol/collection/aov'

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)


    time.sleep(5)
    for i in range(3):  # Scroll down 3 times
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)  # Wait 2 seconds for the page to load more content
    all_content = driver.page_source

    driver.quit()


    file_path = "output_realm.txt"
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(all_content)


def extract_realm_data():
    file_path = "output_realm.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    soup = BeautifulSoup(file_content, 'html.parser')
    script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
    if script_tag:
        # Extract the JSON string
        print("Traversing Script...")
        json_string = script_tag.string
        json_data = json.loads(json_string)

        if 'props' in json_data:
            for page in json_data['props']['pageProps']['dehydratedState']['queries'][4]['state']['data']['pages']:
                print('Token', '\t', 'Level', '\t', 'Magic', '\t', 'Anima', '\t\t', 'Total Cost')
                for token in page['tokens']:
                    # for attrib in token['metadata']['attributes']:
                    #     print(attrib['trait_type'], ' - ', attrib['value'])
                    print(token['priceSummary']['lowestListingObject']['tokenId'], '\t', token['metadata']['attributes'][0]['value'], '\t', int(token['priceSummary']['floorPrice'])/1000000000000000000)
                    # print('Owner - ', token['currentOwner'])


def process_realm_data(goal_level):
    file_path = "manual_realm.txt"
    file = open(file_path, 'r', encoding='utf-8')
    
    adventures = []
    ad = []
    stats = []
    while True:
        line = file.readline()
        if not line:
            break
        if 'View details for' in line:
            numbers = re.findall(r'\d+', line)
            ad.append(numbers[-1])
        elif 'Transcendence Level' in line:
            line = file.readline()
            ad.append(line[:-1])
        elif 'Strength' in line:
            line = file.readline()
            stats.append(int(line[:-1]))
        elif 'Dexterity' in line:
            line = file.readline()
            stats.append(int(line[:-1]))
        elif 'Constitution' in line:
            line = file.readline()
            stats.append(int(line[:-1]))
        elif 'Intelligence' in line:
            line = file.readline()
            stats.append(int(line[:-1]))
        elif 'Wisdom' in line:
            line = file.readline()
            stats.append(int(line[:-1]))
        elif 'Charisma' in line:
            line = file.readline()
            stats.append(int(line[:-1]))
        elif 'Trait Total' in line:
            line = file.readline()
            line = file.readline()
            line = file.readline()
            ad.append(line[:-1])
        elif 'Bid:' in line:
            ad.append(sum(stats))
            adventures.append(ad)
            ad = []
            stats = []
    magic_price = float(get_magic_price())
    anima_price = 0.17
    transaction = 0.5
    print('Total Number of Adventurers: ', len(adventures))
    print('Token', '\t', 'Level', '\t', 'Magic', '\t', 'Anima', '\t', 'Total Cost', '\t', 'Total Stats')
    adv_list = []
    for i in adventures:
        anima_cost = ((32*(goal_level*(goal_level+1)/2) - (29*goal_level)) - (32*(int(i[1])*(int(i[1])+1)/2) - (29*int(i[1]))))
        number_str = float(i[2].replace(',', ''))
        total_costs = (number_str*magic_price + anima_cost*anima_price + transaction*(goal_level-int(i[1])))
        # print(i[0], '\t', i[1], '\t', int(number_str), '\t', anima_cost, '\t', round(total_costs, 2), '\t', i[3])
        adv_list.append([i[0], i[1], int(number_str), anima_cost, round(total_costs, 2), i[3]])
    adv_list.sort(key=lambda x: x[4])
    for j in adv_list:
        print(j[0], '\t', j[1], '\t', j[2], '\t', int(j[3]), '\t', j[4], '\t', j[5])


def save_bigtime_space_data():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # This will suppress most logs
    options.add_argument("--log-level=3")

    url = 'https://openloot.com/marketplace?gameId=56a149cf-f146-487a-8a1c-58dc9ff3a15c&category=space'

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    time.sleep(10)
    # for i in range(3):  # Scroll down 3 times
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        # time.sleep(2)  # Wait 2 seconds for the page to load more content
    all_content = driver.page_source

    driver.quit()


    file_path = "output_bigtime.txt"
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(all_content)


def save_bigtime_time_data():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # This will suppress most logs
    options.add_argument("--log-level=3")

    url = 'https://openloot.com/marketplace?gameId=56a149cf-f146-487a-8a1c-58dc9ff3a15c&search=time+warden'

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    time.sleep(10)
    # for i in range(3):  # Scroll down 3 times
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        # time.sleep(2)  # Wait 2 seconds for the page to load more content
    all_content = driver.page_source

    driver.quit()


    file_path = "output_bigtime_time.txt"
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(all_content)


def extract_bigtime_space_data():
    file_path = "output_bigtime.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    soup = BeautifulSoup(file_content, 'html.parser')
    # script_tag = soup.find_all('div', class_='css-9fxlaj')
    # if script_tag:
    #     for item in script_tag:
    #         print(item)
    script_tag_name = soup.find_all('h2', class_='chakra-heading css-m8b7z0')
    script_tag_price = soup.find_all('p', class_='chakra-text css-29nllk')
    items = []
    if script_tag_name:
        # print("Traversing Script...")
        now = datetime.now()
        items.append({"time": str(now)})
        # print("Time:", now)
        for item in range(len(script_tag_name)):
            soup_name = BeautifulSoup(str(script_tag_name[item]), 'html.parser')
            soup_price = BeautifulSoup(str(script_tag_price[item]), 'html.parser')
            name_tag = soup_name.find('h2')
            price_tag = soup_price.find('p')
            # print('Space:', name_tag.text, '\t', 'Price:', price_tag.text)
            space = {"name": name_tag.text, "price": price_tag.text}
            items.append(space)

    file_path = "results_bigtime_space.json"
    # Open the file in append mode ('a') or write mode ('w')
    with open(file_path, 'a') as file:
        # Iterate over each item in the list and write it to the file
        for item in items:
            file.write(str(item) + ",\n")
    return items


def extract_bigtime_time_data():
    file_path = "output_bigtime_time.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    soup = BeautifulSoup(file_content, 'html.parser')
    # script_tag = soup.find_all('div', class_='css-9fxlaj')
    # if script_tag:
    #     for item in script_tag:
    #         print(item)
    script_tag_name = soup.find_all('h2', class_='chakra-heading css-m8b7z0')
    script_tag_price = soup.find_all('p', class_='chakra-text css-29nllk')
    items = []
    if script_tag_name:
        # print("Traversing Script...")
        now = datetime.now()
        items.append({"time": str(now)})
        # print("Time:", now)
        for item in range(len(script_tag_name)):
            soup_name = BeautifulSoup(str(script_tag_name[item]), 'html.parser')
            soup_price = BeautifulSoup(str(script_tag_price[item]), 'html.parser')
            name_tag = soup_name.find('h2')
            price_tag = soup_price.find('p')
            # print('Space:', name_tag.text, '\t', 'Price:', price_tag.text)
            space = {"name": name_tag.text, "price": price_tag.text}
            items.append(space)

    file_path = "results_bigtime_time.json"
    # Open the file in append mode ('a') or write mode ('w')
    with open(file_path, 'a') as file:
        # Iterate over each item in the list and write it to the file
        for item in items:
            file.write(str(item) + ",\n")
    return items


def display_bigtime_space(store, previous):
    if store != []:
        previous = store
    save_bigtime_space_data()
    store = extract_bigtime_space_data()
    if store != [] and previous != []:
        print('SPACES', store[0]['time'])
        items1 = previous[1:]
        items2 = store[1:]

        dict1 = {item['name']: round(float(item['price'].replace('$', '').replace(',', '').strip())) for item in items1}
        dict2 = {item['name']: round(float(item['price'].replace('$', '').replace(',', '').strip())) for item in items2}

        no_diff = False
        for name, price1 in dict1.items():
            price2 = dict2.get(name)
            if price2 and price1 != price2:
                diff = price2 - price1
                change = (diff*100)/price1
                print(f"Price for {name}: ${price2}, \t Difference: ${diff}, \t % Change: {round(change, 2)}")
                if change < -20:
                    print("ALARMAAAA!!!")
                    root = tk.Tk()
                    root.configure(bg='red')
                    root.attributes('-fullscreen', True)
                    root.bind('<Escape>', lambda e: root.destroy())
                    root.mainloop()
                no_diff = True
        if no_diff == False:
            print("No differences found.")
    return store


def display_bigtime_time(store, previous):
    if store != []:
        previous = store
    save_bigtime_time_data()
    store = extract_bigtime_time_data()
    if store != [] and previous != []:
        print('TIME WARDENS', store[0]['time'])
        items1 = previous[1:]
        items2 = store[1:]

        dict1 = {item['name']: round(float(item['price'].replace('$', '').replace(',', '').strip())) for item in items1}
        dict2 = {item['name']: round(float(item['price'].replace('$', '').replace(',', '').strip())) for item in items2}

        no_diff = False
        for name, price1 in dict1.items():
            price2 = dict2.get(name)
            if price2 and price1 != price2:
                diff = price2 - price1
                change = (diff*100)/price1
                print(f"Price for {name}: ${price2}, \t Difference: ${diff}, \t % Change: {round(change, 2)}")
                if change < -20:
                    print("ALARMAAAA!!!")
                    root = tk.Tk()
                    root.configure(bg='red')
                    root.attributes('-fullscreen', True)
                    root.bind('<Escape>', lambda e: root.destroy())
                    root.mainloop()
                no_diff = True
        if no_diff == False:
            print("No differences found.")
    return store


if __name__ == '__main__':
    if sys.argv[1] == "realm":
        # save_realm_data()
        # extract_realm_data()
        process_realm_data(25)
    elif sys.argv[1] == "bigtime":
        # save_bigtime_space_data()
        # store = extract_bigtime_space_data()
        if sys.argv[2] == "space":
            store = []
            previous = []
            while True:    
                if store != []:
                    previous = store
                save_bigtime_space_data()
                store = extract_bigtime_space_data()
                if store != [] and previous != []:
                    print('SPACES', store[0]['time'])
                    items1 = previous[1:]
                    items2 = store[1:]

                    dict1 = {item['name']: round(float(item['price'].replace('$', '').replace(',', '').strip())) for item in items1}
                    dict2 = {item['name']: round(float(item['price'].replace('$', '').replace(',', '').strip())) for item in items2}

                    no_diff = False
                    for name, price1 in dict1.items():
                        price2 = dict2.get(name)
                        if price2 and price1 != price2:
                            diff = price2 - price1
                            change = (diff*100)/price1
                            print(f"Price for {name}: ${price2}, \t Difference: ${diff}, \t % Change: {round(change, 2)}")
                            if change < -20:
                                print("ALARMAAAA!!!")
                                root = tk.Tk()
                                root.configure(bg='red')
                                root.attributes('-fullscreen', True)
                                root.bind('<Escape>', lambda e: root.destroy())
                                root.mainloop()
                            no_diff = True
                    if no_diff == False:
                        print("No differences found.")
                time.sleep(30)
        elif sys.argv[2] == "time":
            store = []
            previous = []
            while True: 
                if store != []:
                    previous = store
                save_bigtime_time_data()
                store = extract_bigtime_time_data()
                if store != [] and previous != []:
                    print('TIME WARDENS', store[0]['time'])
                    items1 = previous[1:]
                    items2 = store[1:]

                    dict1 = {item['name']: round(float(item['price'].replace('$', '').replace(',', '').strip())) for item in items1}
                    dict2 = {item['name']: round(float(item['price'].replace('$', '').replace(',', '').strip())) for item in items2}

                    no_diff = False
                    for name, price1 in dict1.items():
                        price2 = dict2.get(name)
                        if price2 and price1 != price2:
                            diff = price2 - price1
                            change = (diff*100)/price1
                            print(f"Price for {name}: ${price2}, \t Difference: ${diff}, \t % Change: {round(change, 2)}")
                            if change < -20:
                                print("ALARMAAAA!!!")
                                root = tk.Tk()
                                root.configure(bg='red')
                                root.attributes('-fullscreen', True)
                                root.bind('<Escape>', lambda e: root.destroy())
                                root.mainloop()
                            no_diff = True
                    if no_diff == False:
                        print("No differences found.")
                time.sleep(30)
