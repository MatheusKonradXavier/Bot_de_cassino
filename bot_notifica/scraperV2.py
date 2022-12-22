from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

def pegaValoresKitBlaze() :
  page = requests.get('https://kitblaze.com/double/')
  soup = bs(page.text, "html.parser")
  girosBlaze = soup.find(id="listagem_giros")
  listaValores = list()
  listaHoras = list()
  listaId = list()

  for i in girosBlaze.childGenerator() :
    listaHoras.append(i.get_text()[len(i.get_text())-5:])
    listaValores.append(i.get_text()[:-5])
    listaId.append(i.get('id'))

  df = pd.DataFrame({
    'Valores':listaValores,
    'Horas': listaHoras,
    'Id' : listaId
  })

  return df