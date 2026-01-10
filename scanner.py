import requests as r
import re
from bs4 import BeautifulSoup
class Scan:
    def __init__(self,code):
        self.code = code
        self.mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Décembre"]
    def googleapi(self):
        try:
            info = r.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{self.code}").json()
            self.titre_G = info['items'][0]['volumeInfo']['title']
            self.auteur_G = info['items'][0]['volumeInfo']['authors'][0]
            self.date_G = info['items'][0]['volumeInfo']['publishedDate']
            self.db1 = f"{self.titre_G}{self.auteur_G}"
            return True
        except(KeyError):
            return False
    def bookfinder(self):
        try:
            info = r.get(f"https://www.bookfinder.com/isbn/{self.code}/")
            magnifique_soupe = BeautifulSoup(info.content, 'html.parser')
            self.titre_B = magnifique_soupe.find("h1", class_="text-xl font-bold text-blue-800 mb-2").text
            aut = magnifique_soupe.find("a", class_="text-blue-700 underline font-medium").text
            dat = magnifique_soupe.find_all("div", class_="text-sm mb-1")[1].text.split(", ")[1]
            self.date_B = f"{dat.split("-")[2].lstrip("0")} {self.mois[int(dat.split("-")[1]) -1 ]} {dat.split("-")[0]}" # WIP
            self.auteur_B = f"{aut[aut.find(",") + 2:]} {aut[:aut.find(",")]}"
            self.db2 = f"{self.titre_B}{self.auteur_B}"
            print(f"- Date: {self.date_B}")
            return True
        except(KeyError, AttributeError):
            return False
S = Scan(input("Wsp scan le livre twin\n"))
S.googleapi()
S.bookfinder()
if S.db1:
    if S.db2:
        if re.sub(r"[^a-z0-9]", "", S.db1.lower().strip().replace("é","e")) == re.sub(r"[^a-z0-9]", "", S.db2.lower().strip().replace("é","e")):
            print(f"- Titre: {S.titre_G}\n- Auteur: {S.auteur_G}\n- Date de sortie: {S.date_G}")
        else:
            result = input(f"1: {S.titre_G} par {S.auteur_G} ({S.date_G})\n2: {S.titre_B} par {S.auteur_B} ({S.date_B})\n3: Autre")
    else:
        print(f"- Titre: {S.titre_G}\n- Auteur: {S.auteur_G}\n- Date de sortie: {S.date_G}")
elif S.db2:
    print(f"- Titre: {S.titre_B}\n- Auteur: {S.auteur_B}\n- Date de sortie: {S.date_B}")
else:
    print("Livre introuvable")
    title = input("Veuillez entrer le titre du livre: ")
    auteur = input("Veuillez entrer le nom de l'auteur: ")
    # plugger ça dans la database, pis checker dedans au cas où




# Test ISBN: 9782072947407 (La ferme des animaux de George Orwell, shoutout les cours de français et la révolution russe)
# https://www.googleapis.com/books/v1/volumes?q=isbn:9782072947407
# https://www.bookfinder.com/isbn/9782072947407/
