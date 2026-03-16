import requests as r
import re
from bs4 import BeautifulSoup


class Scan:
    def __init__(self,isbn):
        self.isbn = isbn
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


    def googleapi(self,isbn):
        try:
            info = r.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}").json()
            self.titre_G = info['items'][0]['volumeInfo']['title']
            self.auteur_G = info['items'][0]['volumeInfo']['authors'][0]
            self.language_G = self.lang[info['items'][0]['volumeInfo']['language']]
            dat = info['items'][0]['volumeInfo']['publishedDate']
#            desc = info['items'][0]['volumeInfo']['description']
#            desc_end = desc.find(desc.split(".")[1])                           ### Apparemment inutile ###
#            self.description_G = desc[:desc_end] + "..»"
            self.date_G = f"{dat.split("-")[2].lstrip("0")} {self.mois[int(dat.split("-")[1]) -1 ]} {dat.split("-")[0]}"
            self.db1 = f"{self.titre_G}{self.auteur_G}"
            return True
        except Exception:
            return False

            
    def bookfinder(self,isbn):
        try:
            info = r.get(f"https://www.bookfinder.com/isbn/{isbn}/")
            magnifique_soupe = BeautifulSoup(info.content, 'html.parser')
            self.titre_B = magnifique_soupe.find("h1", class_="text-xl font-bold text-blue-800 mb-2").text
            aut = magnifique_soupe.find("a", class_="text-blue-700 underline font-medium").text
            dat = magnifique_soupe.find_all("div", class_="text-sm mb-1")[1].text.split(", ")[-1]
            lang = magnifique_soupe.find_all("div", class_="text-sm mb-4")[0].text
            self.language_B = self.lang[lang[lang.find(":") + 2:].lower()]
            self.date_B = f"{dat.split("-")[2].lstrip("0")} {self.mois[int(dat.split("-")[1])-1]} {dat.split("-")[0]}" # WIP
            if aut.find(",") > -1:
                self.auteur_B = f"{aut[aut.find(",") + 2:]} {aut[:aut.find(",")]}"
                print("FINDFINFIDNIFNIFN", aut.find(","))
            else:
                self.auteur_B = aut
            self.db2 = f"{self.titre_B}{self.auteur_B}"
            return True
        except Exception:
            return False
    def receiver(self):
        print(f"Scanning ISBN: {self.isbn}")
        if self.googleapi(self.isbn):
#               if re.sub(r"[^a-z0-9]", "", S.db1.lower().strip().replace("é","e")) == re.sub(r"[^a-z0-9]", "", S.db2.lower().strip().replace("é","e")): # Assi inutile -> ISBNs are universal!
            return {"name": self.titre_G,"author": self.auteur_G,"date": self.date_G,"genre": "Non sp\u00e9cifi\u00e9","number": 1}
        elif self.bookfinder(self.isbn):
            return {"name": self.titre_B,"author": self.auteur_B,"date": self.date_B,"genre": "Non sp\u00e9cifi\u00e9","number": 1}
        else:
            return False
            # input nom, auteur, etc. pour mettre dans database (database.py)


# Test ISBN: 9782072947407 (La ferme des animaux de George Orwell, shoutout les cours de français et la révolution russe)
# https://www.googleapis.com/books/v1/volumes?q=isbn:9782072947407
# https://www.bookfinder.com/isbn/9782072947407/


# SECRET 🤫

def remove_all_bugs():
    bugs = False
    works = True
    if bugs == False and works == False:
        print("Oh no, bugs!")
    else:
        pass