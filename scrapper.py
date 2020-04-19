from bs4 import BeautifulSoup
import pymongo
import requests

dbClient = pymongo.MongoClient("mongodb://localhost:27017/")
database = dbClient["test"]
collection = database["testparrafos"]
minimum_paragraph_length = 50

for relato_id in range(50):
    # Page to scrap
    page = requests.get("https://todorelatos.com/relato/" + str(relato_id) + '/')
    soup = BeautifulSoup(page.content, 'html.parser')

    # Find "relato" container
    div_relato = soup.find(id="relato")

    # Check if we have found something. Otherwise just jump to the next "relato"
    if div_relato is None:
        print("Relato #" + str(relato_id) + ' was not found')
        continue

    # Get all items paragraphs
    div_relato_paragraph = div_relato.find_all("p")

    # Convert the html to plain text
    paragraphs_text = []
    for paragraph in div_relato_paragraph:
        paragraphs_text.append(paragraph.getText())

    # Write in database
    paragraph_counter = 1
    for paragraph in paragraphs_text:
        if len(paragraph) > minimum_paragraph_length:
            paragraph_text = paragraph.split('</p>')[0]
            table_entry = {
                "id": str(relato_id),
                "paragraph": str(paragraph_counter),
                "text": paragraph_text
            }
            x = collection.insert_one(table_entry)
            paragraph_counter += 1

print('done')
