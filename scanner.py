import requests as r
import re
from bs4 import BeautifulSoup
class Scan:
    def __init__(self,code):
        self.code = code
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
        #   self.date_B = magnifique_soupe.find_all("span", class_="text-sm md-1").text                                      WIP
            self.auteur_B = f"{aut[aut.find(",") + 2:]} {aut[:aut.find(",")]}"
            self.db2 = f"{self.titre_B}{self.auteur_B}"
            return True
        except(KeyError, AttributeError):
            return False
S = Scan(input("Wsp scan le livre twin\n"))
if S.googleapi():
    if S.bookfinder():
        if re.sub(r"[^a-z0-9]", "", S.db1.lower().strip().replace("é","e")) == re.sub(r"[^a-z0-9]", "", S.db2.lower().strip().replace("é","e")):
            print(f"- Titre: {S.titre_G}\n- Auteur: {S.auteur_G}")
        else:
            result = input(f"1: {S.titre_G} par {S.auteur_G}\n2: {S.titre_B} par {S.auteur_B}\n3: Autre")
    else:
        pass
        # Ouch²
else:
    pass
    # Ouch

    
# Test ISBN: 9782072947407 (La ferme des animaux de George Orwell, shoutout les cours de français et la révolution russe)
# https://www.googleapis.com/books/v1/volumes?q=isbn:9782072947407
# https://www.bookfinder.com/isbn/9782072947407/
