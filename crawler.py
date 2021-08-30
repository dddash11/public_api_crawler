import requests
import time
import sqlite3


class Crawler:
    def __init__(self):
        self.url = "https://public-apis-api.herokuapp.com/api/v1/auth/token"

    def flatten_list(self, _2d_list):
        self.flat_list = []
        # Iterate through the outer list
        for element in _2d_list:
            if type(element) is list:
                # If the element is of type list, iterate through the sublist
                for item in element:
                    self.flat_list.append(item)
            else:
                self.flat_list.append(element)
        return self.flat_list

    def generate_token(self):
        self.url = "https://public-apis-api.herokuapp.com/api/v1/auth/token"
        self.response = requests.get(self.url)
        return self.response.json()['token']

    def get_all_categories(self, token):

        self.categories = []
        self.page = 1
        for i in range(100):

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }

            self.payload = {}
            self.cat_url = f'https://public-apis-api.herokuapp.com/api/v1/apis/categories?page={self.page}'

            self.resp = requests.request(
                "GET", url=self.cat_url, headers=headers, data=self.payload)
            self.data = self.resp.json()['categories']

            if len(self.data) == 0:
                break

            self.categories.append(self.data)
            self.page = self.page + 1

        return self.categories

    def get_all_links(self, all_categories):
        self.items = {}
        self.c = 0

        # time.sleep(60)

        for cat in all_categories:
            time.sleep(60)
            self.t = self.generate_token()
            # print()
            self.items[cat] = {}
            self.enc_cat = self.str_check(cat)

            for i in range(1, 15):

                # handling rate limitation
                if self.c == 9:
                    self.c = 0
                    time.sleep(30)
                    self.t = self.generate_token()

                self.h = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.t}'
                }

                # support for pagination
                self.url = f'https://public-apis-api.herokuapp.com/api/v1/apis/entry?page={i}&category={self.enc_cat}'
                self.r = requests.request(
                    "GET", url=self.url, headers=self.h)

                # print("category = ", cat, "code = ",
                #   self.r.status_code, "page = ", i)
                self.c = self.c+1

                if self.r.status_code != 200:
                    self.t = self.generate_token()

                if len(self.r.json()['categories']) == 0:
                    break

                self.d = self.r.json()['categories']
                for j in range(len(self.d)):
                    self.items[cat][self.d[j]['API']] = self.d[j]['Link']

                # print(self.r.json())
                # if (self.r.headers['X-Ratelimit-Remaining'] == 1):
                # time.sleep(60)
                #self.t = self.generate_token()
        return self.items

    def store_db(self, curr, category, api_name, api_link):
        curr.execute(""" INSERT INTO api_links VALUES (?, ?, ?)""",
                     (
                         category, api_name, api_link
                     )
                     )

    def str_check(self, string):
        if ' ' in string:
            string = string.replace(' ', '+')

        if '&' in string:
            string = string.replace('&', '%26')

        return string


crawler = Crawler()
token = crawler.generate_token()
print("Crawler started")
print("Fetching all api links")
print("Estimated time is 50 minutes. Please wait while this program completes")
categories = crawler.get_all_categories(token)
all_categories = crawler.flatten_list(categories)
items = crawler.get_all_links(all_categories)
my_dict = items
conn = sqlite3.connect("api_links.db")
curr = conn.cursor()
print("Database created")
curr.execute(""" DROP TABLE IF EXISTS api_links""")
curr.execute(""" CREATE TABLE api_links(
    category text,
    api text,
    link text
)""")
for cat in all_categories:
    for val in my_dict[cat].keys():
        crawler.store_db(curr, cat, val, my_dict[cat][val])

conn.commit()
conn.close()
print("Database populated")
print("Crawled all links. Program ends")
