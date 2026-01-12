from flask import Flask, render_template, jsonify
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

@site.route('/execute_script')
def execute_script():
    return "Python script executed!"

if __name__ == '__main__':
    site.run(debug=True, host='0.0.0.0')
