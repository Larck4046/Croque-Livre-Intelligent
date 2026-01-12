// app.js - JavaScript pour Croque-Livre

document.addEventListener('DOMContentLoaded', function() {
    loadBooks();
    setupSearch();
    setupAddSection();
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
                    genre: "Conte philosophique"
                },
                {
                    name: "1984",
                    author: "George Orwell",
                    date: "1949",
                    genre: "Dystopie"
                },
                {
                    name: "Harry Potter à l'école des sorciers",
                    author: "J.K. Rowling",
                    date: "1997",
                    genre: "Fantasy"
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
        `;

        // Ajouter un effet au clic
        card.addEventListener('click', () => {
            alert(`Détails de "${book.name}"\nAuteur: ${book.author}\nDate: ${book.date}\nGenre: ${book.genre}`);
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
    // Toggle buttons
    const toggleScan = document.getElementById('toggle-scan');
    const toggleManual = document.getElementById('toggle-manual');
    const scanMode = document.getElementById('scan-mode');
    const manualMode = document.getElementById('manual-mode');

    toggleScan.addEventListener('click', function() {
        toggleScan.classList.add('active');
        toggleManual.classList.remove('active');
        scanMode.style.display = 'block';
        manualMode.style.display = 'none';
    });

    toggleManual.addEventListener('click', function() {
        toggleManual.classList.add('active');
        toggleScan.classList.remove('active');
        manualMode.style.display = 'block';
        scanMode.style.display = 'none';
    });

    // Scanner functionality
    const startScanBtn = document.getElementById('start-scan');
    const qrScanner = document.getElementById('qr-scanner');

    startScanBtn.addEventListener('click', function() {
        // Placeholder pour le scanner
        qrScanner.classList.add('active');
        qrScanner.innerHTML = '<p>Scanner activé... (Intégrez votre code ici)</p>';

        // Ici, vous intégrerez le code pour html5-qrcode
        // Exemple:
        // const html5QrCode = new Html5Qrcode("qr-scanner");
        // html5QrCode.start(...)

        setTimeout(() => {
            qrScanner.classList.remove('active');
            qrScanner.innerHTML = '<!-- Le scanner sera intégré ici -->';
        }, 5000); // Simuler 5 secondes
    });

    // Manual add form
    const addForm = document.getElementById('manual-add-form');
    addForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const bookData = {
            name: document.getElementById('book-name').value,
            author: document.getElementById('book-author').value,
            date: document.getElementById('book-date').value,
            genre: document.getElementById('book-genre').value
        };

        addBook(bookData);
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