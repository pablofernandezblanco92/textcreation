from bs4 import BeautifulSoup
import requests
import sys
from Helpers.DatabaseAccessor import DatabaseAccessor

# Start Database Connection
da = DatabaseAccessor("mongodb://localhost:27017/", "test", "testparrafos")
da.connect()

'''
links_list = []
for page_number in range(106):
    html = requests.get("https://www.aneroticstory.com/timeline/" + str(page_number)).content
    bs = BeautifulSoup(html, 'html.parser')
    links = bs.find_all("a", {"class": "story"})
    for link in links:
        links_list.append(link['href'])

identifier = 0
for link in links_list:
    print("Collecting resource " + str(identifier) + " out of " + str(len(links_list)))
    html = requests.get(link).content
    bs = BeautifulSoup(html, 'html.parser')
    paragraph_text = bs.find("div", {"class" : "storyContent"}).getText()
    da.insert({
        "id": str(identifier),
        "text": paragraph_text
    })
    identifier += 1
'''


output_file = open('train.txt', 'w')
for paragraph in da.get_gollection().find({}):
    output_file.write(str(paragraph['text'].encode("utf-8")))
    output_file.write("\n")
output_file.close()
