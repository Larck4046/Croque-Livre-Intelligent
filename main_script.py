from flask import Flask, render_template, jsonify, request
import json
import os
from scanner import Scan
from data_base import FileManager

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
    return jsonify({'success': True, 'message': 'Livre ajouté avec succès'})
    # try:
    #     book_data = request.get_json()
        
        # Charger les données existantes
        # if os.path.exists('data_base.json'):
        #     try:
        #         with open('data_base.json', 'r') as f:
        #             data = json.load(f)
        #     except json.JSONDecodeError:
        #         data = []
        # else:
        #     data = []
        
        # Vérifier si le livre existe déjà
    #     existing_book = None
    #     for book in data:
    #         if book['name'].strip().lower() == book_data['name'].strip().lower():
    #             existing_book = book
    #             break
        
    #     if existing_book:
    #         existing_book['number'] += 1
    #     else:
    #         new_book = {
    #             'name': book_data['name'],
    #             'author': book_data['author'],
    #             'date': book_data['date'],
    #             'genre': book_data['genre'],
    #             'number': 1
    #         }
    #         data.append(new_book)
        
    #     # Sauvegarder
    #     with open('data_base.json', 'w') as f:
    #         json.dump(data, f, indent=4)
        
    #     return jsonify({'success': True, 'message': 'Livre ajouté avec succès'})
    # except Exception as e:
    #     return jsonify({'success': False, 'message': str(e)}), 400

@site.route('/api/scan-isbn', methods=['POST'])
def scan_isbn():
    try:
        data = request.get_json()
        isbn = data.get('isbn', '').strip()
        
        if not isbn:
            return jsonify({'success': False, 'message': 'ISBN requis'}), 400
        scanner = Scan(isbn)
        google_success = scanner.googleapi(isbn)
        bookfinder_success = scanner.bookfinder(isbn)

        if google_success and bookfinder_success:
            book_info = {
                'name': scanner.titre_G,
                'author': scanner.auteur_G,
                'date': scanner.date_G,
                'genre': 'Non spécifié'  # On peut ajouter une logique pour déterminer le genre
            }
    except Exception as e:
        pass
    #     """
    #     ICI dawg que le scanner.py est call
    #     """

    #     scanner = Scan.receiver(isbn)
        
    #     # Essayer Google Books API
    #     google_success = scanner.googleapi()
        
    #     # Essayer Bookfinder
    #     bookfinder_success = scanner.bookfinder()
        
    #     book_info = {}
        
    #     if google_success and bookfinder_success:
    #         # Les deux APIs ont réussi, utiliser Google par défaut
    #         book_info = {
    #             'name': scanner.titre_G,
    #             'author': scanner.auteur_G,
    #             'date': scanner.date_G,
    #             'genre': 'Non spécifié'  # On peut ajouter une logique pour déterminer le genre
    #         }
    #     elif google_success:
    #         book_info = {
    #             'name': scanner.titre_G,
    #             'author': scanner.auteur_G,
    #             'date': scanner.date_G,
    #             'genre': 'Non spécifié'
    #         }
    #     elif bookfinder_success:
    #         book_info = {
    #             'name': scanner.titre_B,
    #             'author': scanner.auteur_B,
    #             'date': scanner.date_B,
    #             'genre': 'Non spécifié'
    #         }
    #     else:
    #         return jsonify({'success': False, 'message': 'Livre introuvable avec cet ISBN'}), 404
        
    #     # Ajouter le livre à la base de données
    #     if os.path.exists('data_base.json'):
    #         try:
    #             with open('data_base.json', 'r') as f:
    #                 db_data = json.load(f)
    #         except json.JSONDecodeError:
    #             db_data = []
    #     else:
    #         db_data = []
        
    #     # Vérifier si le livre existe déjà
    #     existing_book = None
    #     for book in db_data:
    #         if book['name'].strip().lower() == book_info['name'].strip().lower():
    #             existing_book = book
    #             break
        
    #     if existing_book:
    #         existing_book['number'] += 1
    #     else:
    #         new_book = {
    #             'name': book_info['name'],
    #             'author': book_info['author'],
    #             'date': book_info['date'],
    #             'genre': book_info['genre'],
    #             'number': 1
    #         }
    #         db_data.append(new_book)
        
    #     # Sauvegarder
    #     with open('data_base.json', 'w') as f:
    #         json.dump(db_data, f, indent=4)
        
    #     return jsonify({
    #         'success': True, 
    #         'message': 'Livre ajouté avec succès',
    #         'book': book_info
    #     })
        
    # except Exception as e:
    #     return jsonify({'success': False, 'message': str(e)}), 500

@site.route('/api/borrow', methods=['POST'])
def borrow_book():
    sorting = FileManager('data_base.json')
    book_data = request.get_json()
    print(book_data)
    sorting.add_remove(1, book_data)
    return jsonify({'success': True, 'message': 'Livre emprunté avec succès'})
    # try:
    #     data = request.get_json()
    #     book_name = data.get('name', '').strip()
        
    #     if not book_name:
    #         return jsonify({'success': False, 'message': 'Nom du livre requis'}), 400
        
    #     # Charger les données
    #     if os.path.exists('data_base.json'):
    #         try:
    #             with open('data_base.json', 'r') as f:
    #                 db_data = json.load(f)
    #         except json.JSONDecodeError:
    #             db_data = []
    #     else:
    #         db_data = []
        
    #     # Trouver le livre
    #     book_found = None
    #     for book in db_data:
    #         if book['name'].strip().lower() == book_name.lower():
    #             book_found = book
    #             break
        
    #     if not book_found:
    #         return jsonify({'success': False, 'message': 'Livre non trouvé'}), 404
        
    #     # Diminuer le nombre
    #     book_found['number'] -= 1
        
    #     if book_found['number'] <= 0:
    #         # Supprimer le livre
    #         db_data.remove(book_found)
        
    #     # Sauvegarder
    #     with open('data_base.json', 'w') as f:
    #         json.dump(db_data, f, indent=4)
        
    #     return jsonify({'success': True, 'message': 'Livre emprunté avec succès'})
        
    # except Exception as e:
    #     return jsonify({'success': False, 'message': str(e)}), 500

@site.route('/execute_script')
def execute_script():
    return "Python script executed!"

if __name__ == '__main__':
    site.run(debug=True, host='0.0.0.0')
