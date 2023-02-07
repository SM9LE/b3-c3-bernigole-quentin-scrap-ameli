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

medecins = soup.find_all("div", class_="item-professionnel")

listeMedecins = []

for medecin in medecins[:50]:
    nomMedecins = medecin.find("div", class_="nom_pictos").text.strip()
    if medecin.find("div", class_="tel") is not None:
        numeroMedecins = medecin.find("div", class_="tel").text.strip()
    adresseMedecins = medecin.find("div", class_="adresse").text.strip()
    listeMedecins.append({"nom": nomMedecins, "numero": numeroMedecins, "adresse": adresseMedecins})

