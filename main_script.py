from flask import Flask, render_template, jsonify, request
import json
import os

site = Flask(__name__)

@site.route('/')
def index():
    return render_template("index.html")

@site.route('/api/books')
def get_books():
    # Charger les livres depuis data_base.json
    if os.path.exists('data_base.json'):
        with open('data_base.json', 'r') as f:
            data = json.load(f)
        # Transformer les données pour le front-end
        books = []
        for book in data:
            books.append({
                'name': book.get('name', 'Titre inconnu'),
                'author': book.get('author', 'Auteur inconnu'),
                'date': book.get('date', 'Date inconnue'),
                'genre': book.get('genre', 'Genre inconnu')
            })
        return jsonify(books)
    else:
        return jsonify([])

@site.route('/api/books', methods=['POST'])
def add_book():
    try:
        book_data = request.get_json()
        
        # Charger les données existantes
        if os.path.exists('data_base.json'):
            with open('data_base.json', 'r') as f:
                data = json.load(f)
        else:
            data = []
        
        # Vérifier si le livre existe déjà
        existing_book = None
        for book in data:
            if book['name'].strip().lower() == book_data['name'].strip().lower():
                existing_book = book
                break
        
        if existing_book:
            existing_book['number'] += 1
        else:
            new_book = {
                'name': book_data['name'],
                'author': book_data['author'],
                'date': book_data['date'],
                'genre': book_data['genre'],
                'number': 1
            }
            data.append(new_book)
        
        # Sauvegarder
        with open('data_base.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        return jsonify({'success': True, 'message': 'Livre ajouté avec succès'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@site.route('/execute_script')
def execute_script():
    return "Python script executed!"

if __name__ == '__main__':
    site.run(debug=True, host='0.0.0.0')
