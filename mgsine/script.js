// ============================================
// DONNÉES DES MAGAZINES
// ============================================

const magazines = [
    {
        id: 1,
        title: 'Numéro 1 - Janvier 2024',
        subtitle: 'L\'accompagnement éducatif au cœur de nos actions',
        image: 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&h=400&fit=crop',
        description: 'Découvrez comment ECLAIR accompagne les jeunes vers le succès académique et professionnel.',
        featured: true,
    },
    {
        id: 2,
        title: 'Numéro 2 - Février 2024',
        subtitle: 'Histoires de mentorat inspirantes',
        image: 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&h=400&fit=crop',
        description: 'Rencontrez nos mentors et leurs protégés qui changent des vies.',
        featured: false,
    },
    {
        id: 3,
        title: 'Numéro 3 - Mars 2024',
        subtitle: 'Développement des compétences',
        image: 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&h=400&fit=crop',
        description: 'Les ateliers de compétences qui préparent les jeunes à l\'emploi.',
        featured: false,
    },
    {
        id: 4,
        title: 'Numéro 4 - Avril 2024',
        subtitle: 'Entrepreneuriat et innovation',
        image: 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&h=400&fit=crop',
        description: 'Comment les jeunes entrepreneurs trouvent leur chemin vers le succès.',
        featured: false,
    },
];

// ============================================
// DOM ELEMENTS
// ============================================

const menuToggle = document.getElementById('menuToggle');
const navMobile = document.getElementById('navMobile');
const searchInput = document.getElementById('searchInput');
const magazinesGrid = document.getElementById('magazinesGrid');
const noResults = document.getElementById('noResults');
const scrollBtn = document.getElementById('scrollBtn');
const featuredMagazine = document.getElementById('featuredMagazine');

// ============================================
// MENU MOBILE
// ============================================

menuToggle.addEventListener('click', () => {
    menuToggle.classList.toggle('active');
    navMobile.classList.toggle('active');
});

// Fermer le menu mobile au clic sur un lien
document.querySelectorAll('.nav-mobile .nav-link').forEach(link => {
    link.addEventListener('click', () => {
        menuToggle.classList.remove('active');
        navMobile.classList.remove('active');
    });
});

// ============================================
// SCROLL VERS MAGAZINES
// ============================================

scrollBtn.addEventListener('click', () => {
    document.getElementById('magazines').scrollIntoView({ behavior: 'smooth' });
});

// ============================================
// RENDU DES MAGAZINES
// ============================================

function renderMagazines(filter = '') {
    const filtered = magazines.filter(mag =>
        mag.title.toLowerCase().includes(filter.toLowerCase()) ||
        mag.subtitle.toLowerCase().includes(filter.toLowerCase())
    );

    // Filtrer les magazines non vedettes
    const nonFeatured = filtered.filter(mag => !mag.featured);

    // Afficher/masquer le message "aucun résultat"
    if (nonFeatured.length === 0) {
        magazinesGrid.innerHTML = '';
        noResults.style.display = filtered.length === 0 ? 'block' : 'none';
        return;
    }

    noResults.style.display = 'none';

    // Rendre les cartes de magazines
    magazinesGrid.innerHTML = nonFeatured.map(magazine => `
        <div class="magazine-card">
            <div class="magazine-card-image">
                <img src="${magazine.image}" alt="${magazine.title}">
            </div>
            <div class="magazine-card-content">
                <h3>${magazine.title}</h3>
                <p class="magazine-card-subtitle">${magazine.subtitle}</p>
                <p class="magazine-card-description">${magazine.description}</p>
                <button class="btn btn-primary" data-magazine="${magazine.title}">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="7 10 12 15 17 10"></polyline>
                        <line x1="12" y1="15" x2="12" y2="3"></line>
                    </svg>
                    Télécharger
                </button>
            </div>
        </div>
    `).join('');

    // Ajouter les event listeners aux boutons de téléchargement
    attachDownloadListeners();
}

// ============================================
// RECHERCHE
// ============================================

searchInput.addEventListener('input', (e) => {
    renderMagazines(e.target.value);
});

// ============================================
// TÉLÉCHARGEMENT PDF
// ============================================

function downloadPDF(magazineTitle) {
    // Créer un canvas pour générer une image
    const canvas = document.createElement('canvas');
    canvas.width = 800;
    canvas.height = 600;
    const ctx = canvas.getContext('2d');

    if (!ctx) return;

    // Fond bleu
    ctx.fillStyle = '#0066CC';
    ctx.fillRect(0, 0, 800, 600);

    // Texte blanc - titre
    ctx.fillStyle = '#FFFFFF';
    ctx.font = 'bold 48px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(magazineTitle, 400, 150);

    // Accent jaune
    ctx.fillStyle = '#FFD700';
    ctx.fillRect(200, 250, 400, 4);

    // Texte descriptif
    ctx.fillStyle = '#FFFFFF';
    ctx.font = '24px Arial';
    ctx.fillText('Magazine OSER', 400, 350);
    ctx.font = '16px Arial';
    ctx.fillText('Édition spéciale', 400, 400);
    ctx.fillText('Téléchargé depuis la plateforme ECLAIR', 400, 500);

    // Convertir en blob et télécharger
    canvas.toBlob((blob) => {
        if (blob) {
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `${magazineTitle.replace(/\s+/g, '_')}.png`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);

            // Afficher une notification
            showNotification(`${magazineTitle} téléchargé avec succès!`);
        }
    });
}

// ============================================
// NOTIFICATIONS
// ============================================

function showNotification(message) {
    // Créer l'élément de notification
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #0066CC;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 1000;
        animation: slideInUp 0.3s ease;
        font-weight: 500;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);

    // Ajouter l'animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    `;
    document.head.appendChild(style);

    // Supprimer la notification après 3 secondes
    setTimeout(() => {
        notification.style.animation = 'slideInUp 0.3s ease reverse';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// ============================================
// ATTACHER LES EVENT LISTENERS AUX BOUTONS
// ============================================

function attachDownloadListeners() {
    document.querySelectorAll('[data-magazine]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const magazineTitle = e.currentTarget.getAttribute('data-magazine');
            downloadPDF(magazineTitle);
        });
    });
}

// ============================================
// INITIALISATION
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    // Rendre les magazines
    renderMagazines();

    // Attacher les event listeners au bouton vedette
    const featuredBtn = featuredMagazine.querySelector('[data-magazine]');
    if (featuredBtn) {
        featuredBtn.addEventListener('click', (e) => {
            const magazineTitle = e.currentTarget.getAttribute('data-magazine');
            downloadPDF(magazineTitle);
        });
    }

    // Ajouter une animation au scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.magazine-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
});

// ============================================
// SCROLL HEADER EFFECT
// ============================================

window.addEventListener('scroll', () => {
    const header = document.querySelector('.header');
    if (window.scrollY > 10) {
        header.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.1)';
    } else {
        header.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
    }
});
