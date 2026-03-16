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
    const stopScanBtn = document.getElementById('stop-scan');
    const scannerContainer = document.getElementById('scanner-container');
    const scannerVideo = document.getElementById('scanner-video');
    const scannerResult = document.getElementById('scanner-result');
    let isScannerActive = false;
    let html5QrCodeInstance = null;

    startScanBtn.addEventListener('click', async function() {
        if (!isScannerActive) {
            isScannerActive = true;
            startScanBtn.style.display = 'none';
            stopScanBtn.style.display = 'inline-block';
            scannerContainer.style.display = 'block';
            scannerResult.innerHTML = '<p style="color: #666;">Initialisation du scanner...</p>';

            await initBarcodeScanner();
        }
    });

    stopScanBtn.addEventListener('click', function() {
        stopBarcodeScanner();
    });

    async function initBarcodeScanner() {
        try {
            // Vérifier si getUserMedia est disponible
            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                scannerResult.innerHTML = '<p style="color: red;">Erreur caméra: Votre navigateur ne supporte pas l\'accès à la caméra. Assurez-vous d\'utiliser HTTPS ou localhost.</p>';
                isScannerActive = false;
                startScanBtn.style.display = 'inline-block';
                stopScanBtn.style.display = 'none';
                scannerContainer.style.display = 'none';
                return;
            }

            // Initialiser html5-qrcode avec configuration optimisée pour EAN-13
            html5QrCodeInstance = new Html5Qrcode("scanner-container");
            
            const config = {
                fps: 10,  // Limite les FPS pour économiser les ressources
                qrbox: { width: 250, height: 150 },  // Zone de scan optimisée pour codes-barres horizontaux
                formatsToSupport: [Html5QrcodeSupportedFormats.EAN_13, Html5QrcodeSupportedFormats.EAN_8]  // Limite aux formats de livres
            };

            await html5QrCodeInstance.start(
                { facingMode: "environment" },  // Utilise la caméra arrière
                config,
                (decodedText, decodedResult) => {
                    // Succès : code-barres détecté
                    console.log('✓ Code-barres détecté:', decodedText);
                    scannerResult.innerHTML = `<p style="color: green;"><strong>✓ Code détecté:</strong> ${decodedText}</p>`;
                    
                    // Ajouter le livre par ISBN/Code-barres
                    scanISBN(decodedText);
                    
                    // Arrêter le scanner
                    if (isScannerActive) {
                        stopBarcodeScanner();
                    }
                },
                (errorMessage) => {
                    // Gestion des erreurs (silencieuse pour éviter le spam)
                    console.warn(`Erreur de scan : ${errorMessage}`);
                }
            ).then(() => {
                console.log("✓ html5-qrcode initialisé");
                scannerResult.innerHTML = '<p style="color: #666;">Scanner actif - placez le code-barres dans la zone</p>';
            }).catch((err) => {
                console.error("Erreur initialisation html5-qrcode:", err);
                scannerResult.innerHTML = `<p style="color: red;">Erreur caméra: ${err.message || err}</p>`;
                isScannerActive = false;
                startScanBtn.style.display = 'inline-block';
                stopScanBtn.style.display = 'none';
                scannerContainer.style.display = 'none';
            });

        } catch (err) {
            console.error('Erreur html5-qrcode:', err);
            scannerResult.innerHTML = `<p style="color: red;">Erreur: ${err.message}</p>`;
            isScannerActive = false;
            startScanBtn.style.display = 'inline-block';
            stopScanBtn.style.display = 'none';
            scannerContainer.style.display = 'none';
        }
    }

    function stopBarcodeScanner() {
        isScannerActive = false;
        startScanBtn.style.display = 'inline-block';
        stopScanBtn.style.display = 'none';
        scannerContainer.style.display = 'none';
        
        try {
            if (html5QrCodeInstance) {
                html5QrCodeInstance.stop().then(() => {
                    console.log("Scanner arrêté");
                }).catch((err) => {
                    console.log("Erreur lors de l'arrêt du scanner:", err);
                });
                html5QrCodeInstance = null;
            }
        } catch (e) {
            console.log("Scanner déjà arrêté");
        }
        
        scannerResult.innerHTML = '<p>Scanner arrêté.</p>';
    }

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
    const submitBtn = document.getElementById('add-book-isbn-btn');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Recherche en cours...';
    submitBtn.disabled = true;

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
        console.error('Erreur:', error);
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
        alert('Erreur lors de la recherche du livre');
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
            alert('Livre emprunté avec succès!');
            // Reload books
            loadBooks();
        } else {
            alert('Erreur: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        alert('Erreur lors de l\'emprunt du livre');
    });
}