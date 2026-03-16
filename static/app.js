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
    const debugModeCheckbox = document.getElementById('debug-mode');
    const debugCanvas = document.getElementById('debug-canvas');
    const debugInfo = document.getElementById('debug-info');
    let isScannerActive = false;
    let html5QrCodeInstance = null;
    let debugMode = false;
    let detectionAttempts = 0;
    let lastErrorMessage = 'Aucune';
    let debugCanvasContext = null;

    startScanBtn.addEventListener('click', async function() {
        console.log('🔄 Bouton démarrer scan cliqué');
        if (!isScannerActive) {
            console.log('📷 Initialisation du scanner...');
            isScannerActive = true;
            detectionAttempts = 0;
            lastErrorMessage = 'Aucune';
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

    // Debug mode toggle
    debugModeCheckbox.addEventListener('change', function() {
        debugMode = this.checked;
        debugCanvas.style.display = debugMode ? 'block' : 'none';
        debugInfo.style.display = debugMode ? 'block' : 'none';
        if (debugMode && !debugCanvasContext) {
            debugCanvasContext = debugCanvas.getContext('2d');
        }
        // Démarrer ou arrêter l'analyse de frames selon le mode debug
        if (debugMode && isScannerActive) {
            startFrameAnalysis();
        }
    });

    async function initBarcodeScanner() {
        console.log('🎥 Fonction initBarcodeScanner appelée');
        console.log('🔍 Protocole:', location.protocol);
        console.log('🏠 Hostname:', location.hostname);
        console.log('📱 UserAgent:', navigator.userAgent);
        
        const isSecure = location.protocol === 'https:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1';
        console.log('🔒 Contexte sécurisé:', isSecure);
        
        try {
            // Vérifier si getUserMedia est disponible
            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                console.error('❌ getUserMedia non disponible');
                scannerResult.innerHTML = '<p style="color: red;">Erreur caméra: Votre navigateur ne supporte pas l\'accès à la caméra. Assurez-vous d\'utiliser HTTPS ou localhost.</p>';
                isScannerActive = false;
                startScanBtn.style.display = 'inline-block';
                stopScanBtn.style.display = 'none';
                scannerContainer.style.display = 'none';
                return;
            }

            console.log('📦 Initialisation html5-qrcode...');
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
                    
                    // Reset debug counters on success
                    detectionAttempts = 0;
                    updateDebugInfo();
                    
                    // Ajouter le livre par ISBN/Code-barres
                    scanISBN(decodedText);
                    
                    // Arrêter le scanner
                    if (isScannerActive) {
                        stopBarcodeScanner();
                    }
                },
                (errorMessage) => {
                    // Gestion des erreurs avec debug
                    detectionAttempts++;
                    lastErrorMessage = errorMessage;
                    
                    if (debugMode) {
                        console.warn(`Erreur de scan (${detectionAttempts}): ${errorMessage}`);
                        updateDebugInfo();
                        
                        // Analyser l'image si en mode debug
                        analyzeCurrentFrame();
                    }
                }
            ).then(() => {
                console.log("✓ html5-qrcode initialisé");
                scannerResult.innerHTML = '<p style="color: #666;">Scanner actif - placez le code-barres dans la zone</p>';
                
                // Initialiser le debug si activé
                if (debugMode) {
                    updateDebugInfo();
                    startFrameAnalysis();
                }
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
        
        // Nettoyer l'intervalle d'analyse de frames
        if (window.frameAnalysisInterval) {
            clearInterval(window.frameAnalysisInterval);
            window.frameAnalysisInterval = null;
        }
        
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

    // Debug helper functions
    function updateDebugInfo() {
        if (!debugMode) return;
        
        document.getElementById('debug-attempts').textContent = `Tentatives: ${detectionAttempts}`;
        document.getElementById('debug-last-error').textContent = `Dernière erreur: ${lastErrorMessage}`;
    }

    function analyzeCurrentFrame() {
        if (!debugMode || !isScannerActive) return;
        
        try {
            // Essayer d'accéder à la vidéo pour analyser l'image
            const videoElement = document.querySelector('#scanner-container video');
            if (!videoElement || videoElement.readyState < 2) return;
            
            if (!debugCanvasContext) {
                debugCanvasContext = debugCanvas.getContext('2d');
            }
            
            // Capturer l'image à pleine résolution pour éviter le flou
            const canvasWidth = 400; // Taille fixe pour le debug
            const canvasHeight = (videoElement.videoHeight / videoElement.videoWidth) * canvasWidth;
            
            debugCanvas.width = canvasWidth;
            debugCanvas.height = canvasHeight;
            
            // Dessiner l'image sans réduction pour éviter le flou
            debugCanvasContext.drawImage(videoElement, 0, 0, canvasWidth, canvasHeight);
            
            // Dessiner la zone de scan simulée (basée sur la config qrbox)
            drawScanZoneOverlay(debugCanvasContext, canvasWidth, canvasHeight);
            
            // Analyser la qualité de l'image sur l'image pleine résolution
            const imageData = debugCanvasContext.getImageData(0, 0, canvasWidth, canvasHeight);
            const quality = analyzeImageQuality(imageData);
            
            document.getElementById('debug-brightness').textContent = `Luminosité: ${quality.brightness.toFixed(1)}%`;
            document.getElementById('debug-contrast').textContent = `Contraste: ${quality.contrast.toFixed(1)}`;
            document.getElementById('debug-focus').textContent = `Netteté: ${quality.sharpness.toFixed(1)}`;
            
            // Feedback visuel basé sur la qualité
            updateQualityFeedback(quality);
            
        } catch (e) {
            console.warn('Erreur analyse image:', e);
        }
    }

    function analyzeImageQuality(imageData) {
        const data = imageData.data;
        let brightness = 0;
        let contrast = 0;
        
        const pixelCount = data.length / 4;
        
        // Calculer la luminosité moyenne
        for (let i = 0; i < data.length; i += 4) {
            const r = data[i];
            const g = data[i + 1];
            const b = data[i + 2];
            const gray = (r + g + b) / 3;
            brightness += gray;
        }
        brightness = (brightness / pixelCount) / 255 * 100;
        
        // Calculer le contraste (écart-type)
        let mean = 0;
        for (let i = 0; i < data.length; i += 4) {
            const gray = (data[i] + data[i + 1] + data[i + 2]) / 3;
            mean += gray;
        }
        mean /= pixelCount;
        
        for (let i = 0; i < data.length; i += 4) {
            const gray = (data[i] + data[i + 1] + data[i + 2]) / 3;
            contrast += Math.pow(gray - mean, 2);
        }
        contrast = Math.sqrt(contrast / pixelCount);
        
        // Calculer la netteté (détection de bords améliorée)
        let sharpness = 0;
        let edgeCount = 0;
        
        // Utiliser un seuil adaptatif pour la détection de bords
        const threshold = mean * 0.1; // 10% du niveau moyen
        
        for (let y = 1; y < imageData.height - 1; y++) {
            for (let x = 1; x < imageData.width - 1; x++) {
                const idx = (y * imageData.width + x) * 4;
                const gray = (data[idx] + data[idx + 1] + data[idx + 2]) / 3;
                
                // Vérifier les voisins horizontaux et verticaux
                const leftIdx = (y * imageData.width + (x-1)) * 4;
                const rightIdx = (y * imageData.width + (x+1)) * 4;
                const topIdx = ((y-1) * imageData.width + x) * 4;
                const bottomIdx = ((y+1) * imageData.width + x) * 4;
                
                const leftGray = (data[leftIdx] + data[leftIdx + 1] + data[leftIdx + 2]) / 3;
                const rightGray = (data[rightIdx] + data[rightIdx + 1] + data[rightIdx + 2]) / 3;
                const topGray = (data[topIdx] + data[topIdx + 1] + data[topIdx + 2]) / 3;
                const bottomGray = (data[bottomIdx] + data[bottomIdx + 1] + data[bottomIdx + 2]) / 3;
                
                // Calculer les gradients
                const gradX = Math.abs(rightGray - leftGray);
                const gradY = Math.abs(bottomGray - topGray);
                const gradient = Math.sqrt(gradX * gradX + gradY * gradY);
                
                // Compter seulement les vrais bords
                if (gradient > threshold) {
                    sharpness += gradient;
                    edgeCount++;
                }
            }
        }
        
        // Normaliser la netteté
        sharpness = edgeCount > 0 ? sharpness / edgeCount : 0;
        
        return { brightness, contrast, sharpness };
    }

    function updateQualityFeedback(quality) {
        let feedback = '';
        let color = '#666';
        
        if (quality.brightness < 30) {
            feedback = '⚠️ Image trop sombre - éclairez mieux';
            color = '#ff9800';
        } else if (quality.brightness > 80) {
            feedback = '⚠️ Image trop claire - réduisez l\'éclairage';
            color = '#ff9800';
        } else if (quality.contrast < 20) {
            feedback = '⚠️ Contraste faible - améliorez l\'éclairage';
            color = '#ff9800';
        } else if (quality.sharpness < 15) {
            feedback = '⚠️ Image floue - tenez l\'appareil stable et rapprochez-vous légèrement';
            color = '#ff9800';
        } else {
            feedback = '✓ Qualité d\'image acceptable - ajustez la distance si la détection échoue';
            color = '#4caf50';
        }
        
        // Ajouter feedback de distance basé sur la taille détectée
        if (detectionAttempts > 5) {
            feedback += '<br>💡 Conseil: Le code-barres doit remplir le rectangle rouge de scan';
        }
        
        if (detectionAttempts > 15) {
            feedback += '<br>🔄 Essayez de tourner le code-barres ou changez d\'angle';
        }
        
        scannerResult.innerHTML = `<p style="color: ${color};">${feedback}</p>`;
    }

    function startFrameAnalysis() {
        if (!debugMode) return;
        
        // Éviter de créer plusieurs intervalles
        if (window.frameAnalysisInterval) {
            clearInterval(window.frameAnalysisInterval);
        }
        
        // Analyser les frames toutes les 500ms
        window.frameAnalysisInterval = setInterval(() => {
            if (isScannerActive && debugMode) {
                analyzeCurrentFrame();
            }
        }, 500);
    }

    function drawScanZoneOverlay(ctx, canvasWidth, canvasHeight) {
        // Récupérer la vidéo pour les dimensions
        const videoElement = document.querySelector('#scanner-container video');
        if (!videoElement) return;
        
        // Simuler la zone de scan (qrbox: { width: 250, height: 150 })
        const scanWidth = 250;
        const scanHeight = 150;
        
        // Calculer les proportions pour s'adapter au canvas
        const scaleX = canvasWidth / videoElement.videoWidth;
        const scaleY = canvasHeight / videoElement.videoHeight;
        
        const scaledScanWidth = scanWidth * scaleX;
        const scaledScanHeight = scanHeight * scaleY;
        
        // Centrer la zone de scan
        const scanX = (canvasWidth - scaledScanWidth) / 2;
        const scanY = (canvasHeight - scaledScanHeight) / 2;
        
        // Dessiner le rectangle de scan
        ctx.strokeStyle = '#ff0000';
        ctx.lineWidth = 3;
        ctx.strokeRect(scanX, scanY, scaledScanWidth, scaledScanHeight);
        
        // Dessiner les coins pour plus de visibilité
        const cornerSize = 20;
        ctx.lineWidth = 4;
        
        // Coin supérieur gauche
        ctx.beginPath();
        ctx.moveTo(scanX, scanY + cornerSize);
        ctx.lineTo(scanX, scanY);
        ctx.lineTo(scanX + cornerSize, scanY);
        ctx.stroke();
        
        // Coin supérieur droit
        ctx.beginPath();
        ctx.moveTo(scanX + scaledScanWidth - cornerSize, scanY);
        ctx.lineTo(scanX + scaledScanWidth, scanY);
        ctx.lineTo(scanX + scaledScanWidth, scanY + cornerSize);
        ctx.stroke();
        
        // Coin inférieur gauche
        ctx.beginPath();
        ctx.moveTo(scanX, scanY + scaledScanHeight - cornerSize);
        ctx.lineTo(scanX, scanY + scaledScanHeight);
        ctx.lineTo(scanX + cornerSize, scanY + scaledScanHeight);
        ctx.stroke();
        
        // Coin inférieur droit
        ctx.beginPath();
        ctx.moveTo(scanX + scaledScanWidth - cornerSize, scanY + scaledScanHeight);
        ctx.lineTo(scanX + scaledScanWidth, scanY + scaledScanHeight);
        ctx.lineTo(scanX + scaledScanWidth, scanY + scaledScanHeight - cornerSize);
        ctx.stroke();
        
        // Ajouter un texte d'aide
        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        ctx.fillRect(scanX, scanY - 25, 200, 20);
        ctx.fillStyle = '#ff0000';
        ctx.font = '12px Arial';
        ctx.fillText('Zone de scan - Placez le code-barres ici', scanX + 5, scanY - 10);
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