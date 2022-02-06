from datetime import date
from pytrends.request import TrendReq
import json

from robot.api.deco import keyword, library


@library(scope='SUITE')
class Trends:
    desktop_terms_list = []
    mobile_terms_list = []

    def __init__(self):
        pass

    @keyword
    def load_search_terms(self, filename='search_terms.json'):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                if data['date'] == date.today().strftime("%b-%d-%Y"):
                    self.desktop_terms_list = data['search_terms']['desktop_terms']
                    self.mobile_terms_list = data['search_terms']['mobile_terms']
                else:
                    generate_term_file()
                    new_data = read_search_terms(filename)
                    self.desktop_terms_list = new_data['desktop_terms']
                    self.mobile_terms_list = new_data['mobile_terms']
        except (FileNotFoundError, KeyError):
            generate_term_file(filename)
            new_data = read_search_terms(filename)
            self.desktop_terms_list = new_data['desktop_terms']
            self.mobile_terms_list = new_data['mobile_terms']

    @keyword
    def get_next_term(self, mode):
        param = mode.casefold()
        valid = ['desktop', 'mobile']
        if param in (option.casefold() for option in valid):
            if param == valid[0]:
                return self.desktop_terms_list.pop()
            else:
                return self.mobile_terms_list.pop()
        raise Exception(f"Parameter must be either {valid[0]} or {valid[1]}, got {mode} instead!")

    def __get_next_desktop_term(self):
        return self.desktop_terms_list.pop()

    def __get_next_mobile_term(self):
        return self.mobile_terms_list.pop()


# END CLASS

def generate_term_file(filename='search_terms.json'):
    response = query_search_terms()
    trend_dict = build_trends()
    search_term_list = response['entityNames'].values()
    desktop_terms, mobile_terms = organize_search_terms(search_term_list)
    trend_dict['search_terms'] = {"desktop_terms": desktop_terms, "mobile_terms": mobile_terms}
    destructive_write_json(trend_dict, filename)


def organize_search_terms(search_term_list):
    desktop_terms = []
    mobile_terms = []
    for index, value in enumerate(search_term_list):
        if len(desktop_terms) < 30:
            desktop_terms.extend(value)
        else:
            if len(mobile_terms) < 20:
                mobile_terms.extend(value)
            else:
                break
    return desktop_terms, mobile_terms


def query_search_terms():
    searches = TrendReq()
    query_dict = searches.realtime_trending_searches(count=50).to_dict()
    return query_dict


def read_search_terms(filename='search_terms.json'):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data['search_terms']


def build_trends():
    trends = {
        "date"        : date.today().strftime("%b-%d-%Y"),
        "times_used"  : 0,
        "search_terms": {
            "desktop": [],
            "mobile" : []
        }
    }
    return trends


def destructive_write_json(data, filename='search_terms.json'):
    with open(filename, 'w+') as file:
        json.dump(data, file, indent=4)
