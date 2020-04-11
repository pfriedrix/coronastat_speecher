import requests
import csv
import pyttsx3
from bs4 import BeautifulSoup

engine = pyttsx3.init()
FILENAME = 'coronavirus_stats.csv'

class Checker:
    def __init__(self):
        self.url_stats = 'https://www.worldometers.info/coronavirus/'
        self.stats = dict()
        self.__manager()

    def __manager(self):
        '''Checker Manager'''
        page = self.get_page()
        self.get_stats_main(page)

    def export(self, type=0):
        '''
        type:0 - default, return stats
        type:1(another integer) - export to csv file
        '''
        if type == 0:
            return self.stats

        fields = [field for field in self.stats.keys()]
        filename = FILENAME

        with open(filename, mode='w') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerow(self.stats)

    def get_page(self):
        try:
             parsed = requests.get(self.url_stats)
        except ConnectionError:
            return False
        if parsed.status_code == 200:
            page = BeautifulSoup(parsed.text, 'html.parser')
            return page
        return False

    def get_stats_main(self, page):
        categories = page.find_all(id='maincounter-wrap')
        for category in categories:
            number = category.find(class_='maincounter-number')
            title = category.find('h1').text.strip()[:-1]
            self.stats[title] = int(number.text.strip().replace(',', ''))


def speecher(value, name_stat):
    if name_stat == 'Coronavirus Cases':
        engine.say('К числу заболевших коронавирусом добавилось {} людей'.format(int(value)))
        engine.runAndWait()
    elif name_stat == 'Deaths':
        engine.say('К числу умерших от коронавируса добавилось {} людей'.format(int(value)))
        engine.runAndWait()
    elif name_stat == 'Recovered':
        engine.say('К числу излечившихся от коронавируса добавилось {} людей'.format(int(value)))
        engine.runAndWait()
    engine.stop()

def detector():
    with open(FILENAME, mode='r') as file:
        prev_stats = csv.DictReader(file)[-1]
        current_stats = checker.export()

        name_stat = str()
        for prev_stat in prev_stats:
            if current_stats[prev_stat[0]] != prev_stat[1]:
                name_stat = prev_stat[0]
                difference = current_stats[prev_stat[0]] - prev_stat[1] 
                speecher(difference, name_stat)
        checker.export(type=1)



if __name__ == "__main__":
    checker = Checker()


