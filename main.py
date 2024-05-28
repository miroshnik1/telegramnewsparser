import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json


def get_first_news():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
    }

    url = "https://www.sjbschool.co.uk/stream/news/full/1/-//"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("li", class_="ps_icon-item ps_itemtype-news-item")


    news_dict = {}

    for article in articles_cards:
        article_title = article.find("h3").text.strip()
        article_desc = article.find("div", class_="ps_activity-information").text.strip()
        article_url = f'https://www.sjbschool.co.uk{article.find("a").get("href")}'

        article_date_time = article.find("span", class_="ps_activity-date").get("datespan")
        date_from_iso = datetime.fromisoformat(article_date_time)
        date_time = datetime.strftime(date_from_iso, "%Y-%m-%d")
        article_date_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d").timetuple())

        article_id = article_url.split("/")[:-1][-1]

        # print(f"{article_title} | {article_url} | {article_date_timestamp}")

        news_dict[article_id] = {
            "article_date_timestamp": article_date_timestamp,
            "article_title": article_title,
            "article_url": article_url,
            "article_desc": article_desc
        }
    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

def check_news_update():
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
    }

    url = "https://www.sjbschool.co.uk/stream/news/full/1/-//"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("li", class_="ps_icon-item ps_itemtype-news-item")

    fresh_news = {}

    for article in articles_cards:
        article_url = f'https://www.sjbschool.co.uk{article.find("a").get("href")}'
        article_id = article_url.split("/")[:-1][-1]

        if article_id in news_dict:
            continue
        else:
            article_title = article.find("h3").text.strip()
            article_desc = article.find("div", class_="ps_activity-information").text.strip()

            article_date_time = article.find("span", class_="ps_activity-date").get("datespan")
            date_from_iso = datetime.fromisoformat(article_date_time)
            date_time = datetime.strftime(date_from_iso, "%Y-%m-%d")
            article_date_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d").timetuple())

            news_dict[article_id] = {
                "article_date_timestamp": article_date_timestamp,
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }

            fresh_news[article_id] = {
                "article_date_timestamp": article_date_timestamp,
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news
def main():
    get_first_news()
    print(check_news_update())

if __name__ == '__main__':
    main()