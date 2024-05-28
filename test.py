# url = "https://www.sjbschool.co.uk/news/detail/year-3-walked-against-hunger-for-cafod/"
#
# article_id = url.split("/")[:-1][-1]
# print(article_id)
import json

with open("news_dict.json") as file:
    news_dict = json.load(file)


search_id = "year-3-walked-against-hunger-for-cafod"

if search_id in news_dict:
    print("I have this one")
else:
    print("NEWNEWNEWNEW")