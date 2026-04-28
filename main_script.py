from flask import Flask, render_template, jsonify, request
import json
import os
import sys
from scanner import Scan, remove_all_bugs
from data_base import FileManager
import threading
from time import sleep
from gpiozero import LED, Button
import evdev

class DoorSystem:
    def __init__(self, relay_pin, sensor_pin, led_v, led_r):
        self.relay = LED(relay_pin)
        self.sensor = Button(sensor_pin)
        self.led_v = LED(led_v)
        self.led_r = LED(led_r)

    def monitor(self):
        while True:
            if self.sensor.is_pressed:
                self.led_v.on()
                self.led_r.off()
            else:
                self.led_v.off()
                self.led_r.on()
            sleep(0.1)

    def open_door(self):
        self.relay.on()
        sleep(0.3)
        self.relay.off()
    def scanner_loop(self):
        while True:
            try:
                event = input()
                print("here")
                print(f"Scanned: {event}")
               	s = Scan(event)
                result = s.receiver()
                if result != False:
                        sorting = FileManager('./data_base.json')
                        sorting.add_remove(0,result)
                        
                        #return jsonify({'success': True, 'book': result})
                else:
            	        #return jsonify({'success': False, 'message': 'Livre introuvable avec cet ISBN'}), 404
                        pass
                del s
            except EOFError:
                pass

door = DoorSystem(5, 13, 6, 12)

site = Flask(__name__)

@site.route('/')
def index():
    return render_template("index.html")

@site.route('/api/books')
def get_books():
    # Charger les livres depuis data_base.json
    if os.path.exists('data_base.json'):
        try:
            with open('data_base.json', 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []
        # Transformer les données pour le front-end
        books = []
        for book in data:
            books.append({
                'name': book.get('name', 'Titre inconnu'),
                'author': book.get('author', 'Auteur inconnu'),
                'date': book.get('date', 'Date inconnue'),
                'genre': book.get('genre', 'Genre inconnu'),
                'number': book.get('number', 1)
            })
        return jsonify(books)
    else:
        return jsonify([])

@site.route('/api/books', methods=['POST'])
def add_book():
    sorting = FileManager('data_base.json')
    book_data = request.get_json()
    sorting.add_remove(0, book_data)
    print(book_data)
    door.open_door()
    return jsonify({'success': True, 'message': 'Livre ajouté avec succès'})

@site.route('/api/scan-isbn', methods=['POST'])
def scan_isbn():
    try:
        data = request.get_json()
        isbn = data.get('isbn', '').strip()
        
        if not isbn:
            return jsonify({'success': False, 'message': 'ISBN requis'}), 400
        scanner = Scan(isbn)
        result = scanner.receiver()

   #     google_success = scanner.googleapi(isbn)
   #     bookfinder_success = scanner.bookfinder(isbn)
        if result != False:
            sorting = FileManager('data_base.json')
            sorting.add_remove(0,result)
            return jsonify({'success': True, 'book': result})
        else:
            return jsonify({'success': False, 'message': 'Livre introuvable avec cet ISBN'}), 404

    except Exception as e:
        pass

@site.route('/api/borrow', methods=['POST'])
def borrow_book():
    sorting = FileManager('data_base.json')
    book_data = request.get_json()
    print(book_data)
    sorting.add_remove(1, book_data)
    door.open_door()
    return jsonify({'success': True, 'message': 'Livre emprunté avec succès'})
    

@site.route('/execute_script')
def execute_script():
    return "Python script executed!"

if __name__ == '__main__':
    cert_file = 'cert.pem'
    key_file = 'key.pem'
    
    # Check if certificate files exist
    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        print(f"\n⚠️  Certificate files not found!")
        print(f"Please run: python generate_cert.py")
        print(f"Then start the server again.\n")
        sys.exit(1)
    
    threading.Thread(target=door.monitor, daemon=True).start()
    threading.Thread(target=door.scanner_loop, daemon=True).start()
    site.run(debug=False, host='0.0.0.0', port=5002)
