from bs4 import BeautifulSoup
import pymongo
import requests

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["test"]
mycol = mydb["testparrafos"]
longitud_minima_parrafo = 50

for id in range(1000):
  try:
    #Page to scrap
    page = requests.get("https://todorelatos.com/relato/" + str(id) + '/')

    soup = BeautifulSoup(page.content, 'html.parser')
    
    #Division on paragrafs
    divided_soup = str(soup).split('<p align="justify">')
    parrafos = divided_soup[1:-1]
    
    #Append last paragraf
    parrafos.append(divided_soup[-1].split('</div>')[0])
    
    #Write in bbdd
    counter_parrafos = 1
    for parrafo in parrafos:
      if len(parrafo) > longitud_minima_parrafo:
        texto_parrafo = parrafo.split('</p>')[0]
        mydict = { "id": str(id), "paragrafo": str(counter_parrafos), "texto": texto_parrafo }
        x = mycol.insert_one(mydict)
        counter_parrafos += 1

  except:
    pass
    print(str(id) +' failed')
    
print('done')