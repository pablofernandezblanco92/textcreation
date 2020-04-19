from bs4 import BeautifulSoup
import pymongo
import requests

dbClient = pymongo.MongoClient("mongodb://localhost:27017/")
database = dbClient["test"]
collection = database["testparrafos"]
minimum_paragraph_length = 50

for id in range(1000):
  try:
    # Page to scrap
    page = requests.get("https://todorelatos.com/relato/" + str(id) + '/')
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # Division on paragraphs
    divided_soup = str(soup).split('<p align="justify">')
    paragraphs = divided_soup[1:-1]
    
    # Append last paragraphs
    paragraphs.append(divided_soup[-1].split('</div>')[0])
    
    # Write in database
    paragraph_counter = 1
    for paragraph in paragraphs:
      if len(paragraph) > minimum_paragraph_length:
        paragraph_text = paragraph.split('</p>')[0]
        table_entry = {
          "id": str(id),
          "paragraph": str(paragraph_counter),
          "text": paragraph_text
        }
        x = collection.insert_one(table_entry)
        paragraph_counter += 1
  except:
    pass
    print(str(id) + ' failed')
    
print('done')
