// app.js - JavaScript pour Croque-Livre

document.addEventListener('DOMContentLoaded', function() {
    loadBooks();
    setupSearch();
    setupAddSection();
    // Auto-refresh books every 5 seconds
    setInterval(loadBooks, 5000);
});

function loadBooks() {
    fetch('/api/books')
        .then(response => response.json())
        .then(books => {
            displayBooks(books);
        })
        .catch(error => {
            console.error('Erreur lors du chargement des livres:', error);
            // Fallback aux données d'exemple
            const sampleBooks = [
                {
                    name: "Le Petit Prince",
                    author: "Antoine de Saint-Exupéry",
                    date: "1943",
                    genre: "Conte philosophique",
                    number: 3
                },
                {
                    name: "1984",
                    author: "George Orwell",
                    date: "1949",
                    genre: "Dystopie",
                    number: 2
                },
                {
                    name: "Harry Potter à l'école des sorciers",
                    author: "J.K. Rowling",
                    date: "1997",
                    genre: "Fantasy",
                    number: 1
                }
            ];
            displayBooks(sampleBooks);
        });
}

function displayBooks(books) {
    const container = document.getElementById('books-container');
    container.innerHTML = '';

    books.forEach(book => {
        const card = document.createElement('div');
        card.className = 'book-card';
        card.innerHTML = `
            <div class="book-title">${book.name}</div>
            <div class="book-author">Auteur: ${book.author}</div>
            <div class="book-date">Date de publication: ${book.date}</div>
            <div class="book-genre">Genre: ${book.genre}</div>
            <div class="book-number">Exemplaires: ${book.number}</div>
            <button class="book-remover">Emprunter</button>
        `;

        // Ajouter un effet au clic sur la carte (sauf le bouton)
        card.addEventListener('click', (e) => {
            if (e.target.className !== 'book-remover') {
                alert(`Détails de "${book.name}"\nAuteur: ${book.author}\nDate: ${book.date}\nGenre: ${book.genre}\nExemplaires: ${book.number}`);
            }
        });

        // Bouton emprunter
        const borrowBtn = card.querySelector('.book-remover');
        borrowBtn.addEventListener('click', () => {
            borrowBook(book.name);
        });

        container.appendChild(card);
    });
}

function setupSearch() {
    const searchInput = document.getElementById('search-input');
    searchInput.addEventListener('input', function() {
        const query = this.value.toLowerCase();
        const cards = document.querySelectorAll('.book-card');

        cards.forEach(card => {
            const title = card.querySelector('.book-title').textContent.toLowerCase();
            const author = card.querySelector('.book-author').textContent.toLowerCase();
            const visible = title.includes(query) || author.includes(query);
            card.style.display = visible ? 'block' : 'none';
        });
    });
}

function setupAddSection() {
    // Manual add form
    const addForm = document.getElementById('manual-add-form');
    addForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const bookData = {
            name: document.getElementById('book-name').value,
            author: document.getElementById('book-author').value,
            date: document.getElementById('book-date').value,
            genre: document.getElementById('book-genre').value,
            number: 1
        };

        addBook(bookData);
    });

    // ISBN scan form
    const isbnForm = document.getElementById('manual-add-isbn');
    const isbnInput = document.getElementById('book-isbn');
    
    // Auto-submit when 13 characters are reached
    isbnInput.addEventListener('input', function() {
        if (this.value.length === 13) {
            isbnForm.dispatchEvent(new Event('submit'));
        }
    });
    
    isbnForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const isbn = isbnInput.value.trim();
        
        if (!isbn) {
            alert('Veuillez entrer un code ISBN');
            return;
        }

        scanISBN(isbn);
    });
}

function addBook(bookData) {
    fetch('/api/books', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(bookData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Livre ajouté avec succès!');
            // Clear form
            document.getElementById('manual-add-form').reset();
            // Reload books
            loadBooks();
        } else {
            alert('Erreur lors de l\'ajout du livre: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        alert('Erreur lors de l\'ajout du livre');
    });
}

function scanISBN(isbn) {
    // Afficher un message de chargement
    // const submitBtn = document.getElementById('add-book-isbn-btn');
    // const originalText = submitBtn.textContent;
    // submitBtn.textContent = 'Recherche en cours...';
    // submitBtn.disabled = true;

    fetch('/api/scan-isbn', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ isbn: isbn })
    })
    .then(response => response.json())
    .then(data => {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;

        if (data.success) {
            alert(`Livre trouvé et ajouté!\nTitre: ${data.book.name}\nAuteur: ${data.book.author}\nDate: ${data.book.date}`);
            // Clear ISBN form
            document.getElementById('manual-add-isbn').reset();
            // Reload books
            loadBooks();
        } else {
            alert('Erreur: ' + data.message);
        }
    })
    .catch(error => {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
        console.error('Erreur:', error);
        alert('Erreur lors de la recherche ISBN');
    });
}

function borrowBook(bookName) {
    fetch('/api/borrow', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: bookName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // alert('Livre emprunté avec succès!');
            // Reload books
            loadBooks();
        } else {
            alert('Erreur lors de l\'emprunt: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        alert('Erreur lors de l\'emprunt');
    });

}
