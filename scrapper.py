from Helpers.DatabaseAccessor import DatabaseAccessor
from Helpers.RelatoScrapper import RelatoScrapper

# Define constants
MINIMUM_PARAGRAPH_LENGTH = 50

# Start Database Connection
da = DatabaseAccessor("mongodb://localhost:27017/", "test", "testparrafos")
da.connect()

# Iterate over all the "relatos"
for relato_id in range(50):
    # Page to scrap
    scrapper = RelatoScrapper("https://todorelatos.com/relato/" + str(relato_id) + '/')
    scrapper.obtain_html()

    # Check if we have found something. Otherwise just jump to the next "relato"
    if not scrapper.is_valid():
        print("Relato #" + str(relato_id) + ' was not found')
        continue
    else:
        print("Relato #" + str(relato_id) + ' found. Starting scrapping...')

    # Start paragraph scrapping
    scrapper.obtain_paragraphs()

    # Write in database
    paragraph_counter = 1
    for paragraph in scrapper.transform_paragraphs_to_plain_text():
        if len(paragraph) > MINIMUM_PARAGRAPH_LENGTH:
            paragraph_text = paragraph.split('</p>')[0]
            da.insert({
                "id": str(relato_id),
                "paragraph": str(paragraph_counter),
                "text": paragraph_text
            })
            paragraph_counter += 1

da.close()
print('done')
