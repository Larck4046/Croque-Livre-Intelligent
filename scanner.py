import requests as r
from bs4 import BeautifulSoup


class Scan:
    def __init__(self, isbn):
        self.isbn = isbn
        self.lang = {
            "french": "Français",
            "fr": "Français",
            "en": "Anglais",
            "english": "Anglais",
            "es": "Español",
            "spanish": "Español",
            "it": "Italien",
            "italian": "Italien",
            "ko": "Coréen",
            "korean": "Coréen",
            "ja": "Japonais",
            "japanese": "Japonais",
            "de": "Allemand",
            "german": "Allemand",
            "la": "Latin",
            "latin": "Latin",
            "ru": "Russe",
            "russian": "Russe",
            "vi": "Vietnamien",
            "vietnamese": "Vietnamien",
            "he": "Hébreu",
            "hebrew": "Hébreu",
            "ar": "Arabe",
            "arabic": "Arabe",
        }
        self.mois = [
            "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
            "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
        ]

    def _format_date(self, dat):
        parts = dat.split("-")
        if len(parts) == 3:
            year, month, day = parts
            return f"{day.lstrip('0')} {self.mois[int(month) - 1]} {year}"
        return dat

    def googleapi(self, isbn):
        try:
            info = r.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}").json()
            if "items" not in info or len(info["items"]) == 0:
                print(f"ISBN {isbn} non trouvé dans Google Books")
                return False
            
            volume = info["items"][0]["volumeInfo"]

            self.titre_G = volume.get("title", "Inconnu")
            authors = volume.get("authors", ["Auteur inconnu"])
            self.auteur_G = authors[0]
            self.language_G = self.lang.get(volume.get("language", "").lower(), "Inconnu")
            self.date_G = self._format_date(volume.get("publishedDate", "Inconnu"))
            self.db1 = f"{self.titre_G}{self.auteur_G}"
            if self.titre_G == "Inconnu" or self.auteur_G == "Auteur inconnu":
                print(f"Google Books n'a pas pu trouver les informations pour ISBN {isbn}")
                return False
            return True
        except Exception as e:
            print(f"Erreur Google Books: {e}")
            return False

    def bookfinder(self, isbn):
        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                )
            }
            info = r.get(f"https://www.bookfinder.com/isbn/{isbn}/", headers=headers)
            info.encoding = "utf-8"
            soup = BeautifulSoup(info.text, "html.parser")

            title_tag = soup.find("h1", class_="text-xl font-bold text-blue-800 mb-2")
            author_tag = soup.find("a", class_="text-blue-700 underline font-medium")
            meta = soup.find_all("div", class_="text-sm mb-1")
            lang_meta = soup.find_all("div", class_="text-sm mb-4")

            self.titre_B = title_tag.text.strip() if title_tag else "Inconnu"
            aut = author_tag.text.strip() if author_tag else "Auteur inconnu"

            dat = "Inconnu"
            if len(meta) > 1:
                dat = meta[1].text.split(", ")[-1]

            lang = "Inconnu"
            if lang_meta:
                raw_lang = lang_meta[0].text
                if ":" in raw_lang:
                    lang = raw_lang[raw_lang.find(":") + 1:].strip().lower()
            self.language_B = self.lang.get(lang, "Inconnu")
            self.date_B = self._format_date(dat)

            if "," in aut:
                last, first = aut.split(",", 1)
                self.auteur_B = f"{first.strip()} {last.strip()}"
            else:
                self.auteur_B = aut

            self.db2 = f"{self.titre_B}{self.auteur_B}"
            return True
        except Exception as e:
            print(f"Erreur dans bookfinder: {e}")
            return False

    def receiver(self):
        print(f"Scanning ISBN: {self.isbn}")
        if self.googleapi(self.isbn):
            if self.titre_G != "Inconnu":
                return {
                    "name": self.titre_G,
                    "author": self.auteur_G,
                    "date": self.date_G,
                    "genre": "Non spécifié",
                    "number": 1,
                }
            else:
                print(f"Titre inconnu pour ISBN {self.isbn} (Google Books)")
        
        if self.bookfinder(self.isbn):
            if self.titre_B != "Inconnu":
                return {
                    "name": self.titre_B,
                    "author": self.auteur_B,
                    "date": self.date_B,
                    "genre": "Non spécifié",
                    "number": 1,
                }
            else:
                print(f"Titre inconnu pour ISBN {self.isbn} (BookFinder)")
        
        return False