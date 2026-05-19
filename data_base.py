"""

Si tu veux modifier qqch Feel Free! Et si tu as des questions, pose les ici
Jumeau t’es un génie
"""
"""
WOW
"""

import json
import os
import shutil
from time import sleep
class FileManager:
    def __init__(self, path):
        self.path = path

    def load_data(self):
        if os.path.exists(self.path) and os.path.getsize(self.path) > 0:
            try:
                with open(self.path, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("⚠️ JSON file corrupted — starting fresh.")
                with open('data_base.json.old', "r") as file:
                    return json.load(file)
        return []
    def save_data(self,saved_data):
        self.data = saved_data
        with open(self.path, "w") as file:
            json.dump(self.data, file, indent=4)
        print("Database saved.")
    
    def quit(self):
        shutil.copy('data_base.json', 'data_base.json.old')
    
    def add_remove(self,choice,data):
        # Non-interactive dispatcher for web/API usage.
        if choice == 0:
            check(self, data)
        elif choice == 1:
            remove(self, data)
        elif choice == 2:
            searching(self)
        elif choice == 3 or choice is None:
            exit_prog(self)
        else:
            # Unknown choice: no-op
            pass
            




def check(manager,data):
    number = 1
    found = False
    db = manager.load_data()
    name = data["name"]
    genre = data["genre"]
    author = data["author"]
    date = data["date"]

    # Find and update existing entry
    for book in db:
        
        if book["name"].strip().lower() == name.strip().lower():
            
            book["number"] += 1
            number = book["number"]
            found = True
            print(f"Updated '{name}' to number {number}")
            break

    if not found:
        db.append({"name": name, "genre": genre, "author": author, "date": date, "number": number})
        print(f"Added new book '{name}' as number {number}")

    manager.save_data(db)


def remove(manager, data):
    clear_terminal()
    found = False
    db = manager.load_data()

    choice = data["name"]

    #removing section
    for book in db:
        if book["name"] == choice:
            found = True
            a=book["number"]
            print(a)
            if book["number"] > 1:
                book["number"] -= 1
            else:
                db.remove(book)
    print(f"Removing book: {choice}")
    if not found:
        print("Didn't found book, passing")
        
    manager.save_data(db)
def searching(manager):
    clear_terminal()
    data = manager.load_data()
    accepted = True
    
    while accepted == True:
        choice = input('Searchin by: name or genre?')
        if choice == 'name':
            for book in data:
                clear_terminal()
                print(f"Name: {book['name']}, Author: {book.get('author', 'Unknown')}, Date: {book.get('date', 'Unknown')}")
                accepted = False
                
        elif choice == 'genre':
            for book in data:
                clear_terminal()
                print(f"Genre: {book['genre']}, Name: {book['name']}")
                accepted = False
    
        
    
def exit_prog(manager):
    clear_terminal()
    manager.quit()
def clear_terminal():
    # For Windows
    if os.name == "nt":
        _ = os.system("cls")
    # For macOS and Linux (Unix-like systems)
    else:
        _ = os.system("clear")







