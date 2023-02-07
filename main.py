import requests
from bs4 import BeautifulSoup
import csv

url = "http://annuairesante.ameli.fr/recherche.html"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/189.8.0.8 Safari/537.36"
}

req = requests.session()
payload= {
    "type": "ps",
    "ps_profession" : "34",
    "ps_profession_label": "Médecin généraliste",
    "ps_localisation": "HERAULT (34)",
    "localisation_category": "departements",
}

page = req.post(url, params=payload, headers=header)

if page.status_code == 200:
    lienrecherche = page.url

soup = BeautifulSoup(page.text, 'html.parser')

# Récupérer tous les noms des médecins
classe_noms = "ignore-css"
tousLesNoms = soup.find_all("h2", class_=classe_noms)
noms = []
for nom in tousLesNoms:
    noms.append(nom.string)
    print(nom)

print(soup)

# Récupérer tous les numéros des médecins
classe_numeros = "item.left.tel"
tousLesNums = soup.find_all("div", class_=classe_numeros)
numeros = []
for numero in tousLesNums:
    numeros.append(numero.string)
    print(numero)

print('--------------------------')

# Récupérer toutes les adresses des médecins
classe_adresses = "item.left.adresse"
toutesLesAddresses = soup.find_all("div", class_=classe_adresses)
adresses = []
for adresse in toutesLesAddresses:
    adresses.append(adresse.string)

print('--------------------------')

# Création du fichier csv "medecins_generalistes.csv"
en_tete = ['nom', 'numero', 'adresse']
with open('medecins_generalistes.csv') as fichier_csv:
    writer = csv.writer(fichier_csv, delimiter=";")
    writer.writerow(en_tete)
    for nom, numero, adresse in zip(noms, numeros, adresses):
        writer.writerow([nom, numero, adresse])
