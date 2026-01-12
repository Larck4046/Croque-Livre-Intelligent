"""

Si tu veux modifier qqch Feel Free! Et si tu as des questions, pose les ici
Jumeau t’es un génie
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
    
        
        
def add_remove():
    print("Oublie pas de sauvegarder dans le fichier Anthony!!!")
    
    while True:
        path = '/api/books.json'
        manager = FileManager(path)
        
        choice = input("Select between adding or removing a book (add/remove/searching/quit)")
        
        if choice.strip().lower() == "add":
            check(manager)
            sleep(1)
        elif choice.strip().lower() == "remove":
            remove(manager)
            sleep(1)
        elif choice.strip().lower() == "searching":
            searching(manager)
            sleep(1)
        elif choice.strip().lower() == "quit":
            exit_prog(manager)
            break
        else:
            pass
            




def check(manager):
    number = 1
    found = False
    data = manager.load_data()
    name = input("name: ")
    genre = input("genre: ")
    author = input("author: ")
    date = input("date: ")
    
    # Find and update existing entry
    for book in data:
        
        if book["name"].strip().lower() == name.strip().lower():
            
            book["number"] += 1
            number = book["number"]
            found = True
            print(f"Updated '{name}' to number {number}")
            break

    if not found:
        data.append({"name": name, "genre": genre, "author": author, "date": date, "number": number})
        print(f"Added new book '{name}' as number {number}")

    manager.save_data(data)


def remove(manager):
    clear_terminal()
    found = False
    data = manager.load_data()

    #Shows all books in data base
    print("Choose between one of those books:")
    for book in data:
        print(f"Name: {book['name']}, Number: {book['number']}")
    choice = input()

    #removing section
    for book in data:
        if book["name"] == choice:
            found = True
            if book["number"] > 1:
                book["number"] -= 1
            else:
                data.remove(book)
    if not found:
        print("Didn't found book, passing")
        
    manager.save_data(data)

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



    


add_remove()





