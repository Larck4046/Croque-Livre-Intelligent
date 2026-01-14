import requests as r
import re
from bs4 import BeautifulSoup
class Scan:
    def __init__(self,code):
        self.code = code
        self.lang = {
            "french":"Français",
            "fr":"Français",
            "en":"Anglais",
            "english":"Anglais",
            "es":"Español",
            "spanish":"Español",
            "it":"Italien",
            "italian":"Italien",
            "ko":"Coréen",
            "korean":"Coréen",
            "ja":"Japonais",
            "japanese":"Japonais",
            "de":"Allemand",
            "German":"Allemand",
            "la":"Latin",
            "latin":"Latin",
            "ru":"Russe",
            "russian":"Russe",
            "vi":"Vietnamien",
            "vietnamese":"Vietnamien",
            "he":"Hébreu",
            "hebrew":"Hébreu",
            "ar":"Arabe",
            "arabic":"Arabe"
        }
        self.mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    def googleapi(self):
        try:
            info = r.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{self.code}").json()
            self.titre_G = info['items'][0]['volumeInfo']['title']
            self.auteur_G = info['items'][0]['volumeInfo']['authors'][0]
            self.language_G = self.lang[info['items'][0]['volumeInfo']['language']]
            dat = info['items'][0]['volumeInfo']['publishedDate']
            desc = info['items'][0]['volumeInfo']['description']
            desc_end = desc.find(desc.split(".")[1])
            self.description_G = desc[:desc_end] + "..»"
            self.date_G = f"{dat.split("-")[2].lstrip("0")} {self.mois[int(dat.split("-")[1]) -1 ]} {dat.split("-")[0]}"
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
            dat = magnifique_soupe.find_all("div", class_="text-sm mb-1")[1].text.split(", ")[-1]
            lang = magnifique_soupe.find_all("div", class_="text-sm mb-4")[0].text
            self.language_B = self.lang[lang[lang.find(":") + 2:].lower()]
            self.date_B = f"{dat.split("-")[2].lstrip("0")} {self.mois[int(dat.split("-")[1])-1]} {dat.split("-")[0]}" # WIP
            self.auteur_B = f"{aut[aut.find(",") + 2:]} {aut[:aut.find(",")]}"
            self.db2 = f"{self.titre_B}{self.auteur_B}"
            return True
        except(KeyError, AttributeError):
            return False


            
S = Scan(input("Wsp scan le livre twin\n"))
if S.googleapi():
    if S.bookfinder():
        if re.sub(r"[^a-z0-9]", "", S.db1.lower().strip().replace("é","e")) == re.sub(r"[^a-z0-9]", "", S.db2.lower().strip().replace("é","e")):
            print(f"- Titre: {S.titre_G}\n- Auteur: {S.auteur_G}\n- Date de sortie: {S.date_G}\n- Langue: {S.language_G}\n- Description: {S.description_G}")
        else:
            print("NOT match")
            result = input(f"1: {S.titre_G} par {S.auteur_G} ({S.date_G})\n2: {S.titre_B} par {S.auteur_B} ({S.date_B})\n3: Autre")
            # Input handling, database pulling, bars flowing
    else:
        print("GoogleAPI")
        print(f"- Titre: {S.titre_G}\n- Auteur: {S.auteur_G}\n- Date de sortie: {S.date_G}\n- Langue: {S.language_G}\n- Description: {S.description_G}")
elif S.bookfinder():
    print("Bookfinder")
    print(f"- Titre: {S.titre_B}\n- Auteur: {S.auteur_B}\n- Date de sortie: {S.date_B}\n- Langue: {S.language_B}")
else:
    print("Livre introuvable parmi 190 millions de livres")
    # input nom, auteur, etc. pour mettre dans database (database.py)


# Test ISBN: 9782072947407 (La ferme des animaux de George Orwell, shoutout les cours de français et la révolution russe)
# https://www.googleapis.com/books/v1/volumes?q=isbn:9782072947407
# https://www.bookfinder.com/isbn/9782072947407/
