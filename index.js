// List of taxonomy files to load
const taxonomyFiles = [
    'surveys.json',
    'data-balancing.json',
    'neural-architecture.json',
    'feature-enrichment.json',
    'logits-adjustment.json',
    'loss-functions.json',
    'foundation-models.json',
    'multimodality.json',
    'fairness.json',
    'rare-disease.json'
];

let allPapers = 0;
let allCategories = 0;

// Load all taxonomy files
async function loadTaxonomies() {
    const content = document.getElementById('content');
    content.innerHTML = '';

    for (const file of taxonomyFiles) {
        try {
            const response = await fetch(`taxonomies/${file}`);
            const data = await response.json();
            renderTaxonomy(data);
            allCategories++;
            allPapers += data.papers.length;
        } catch (error) {
            console.error(`Error loading ${file}:`, error);
        }
    }

    updateStats();
}

// Render a taxonomy section
function renderTaxonomy(taxonomy) {
    const content = document.getElementById('content');

    const section = document.createElement('section');
    section.className = 'taxonomy-section';

    section.innerHTML = `
        <div class="section-header">
            <div>
                <h2 class="section-title">${taxonomy.category}</h2>
                ${taxonomy.description ? `<p class="section-description">${taxonomy.description}</p>` : ''}
            </div>
            <span class="paper-count">${taxonomy.papers.length} papers</span>
        </div>
        <div class="papers-grid">
            ${taxonomy.papers.map(paper => renderPaperCard(paper)).join('')}
        </div>
    `;

    content.appendChild(section);
}

// Render a paper card
function renderPaperCard(paper) {
    const authors = formatAuthors(paper.authors);
    const searchQuery = encodeURIComponent(`${paper.title} ${authors.split(',')[0]} ${paper.year}`);
    const scholarUrl = `https://scholar.google.com/scholar?q=${searchQuery}`;

    return `
        <div class="paper-card">
            <h4 class="paper-title">${paper.title}</h4>
            <p class="paper-authors">${authors}</p>
            <div class="paper-meta">
                <span class="paper-year">${paper.year}</span>
                ${paper.venue ? `<span class="paper-venue">${paper.venue}</span>` : ''}
            </div>
            <div class="paper-actions">
                <a href="${scholarUrl}" target="_blank" class="btn btn-scholar">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 24a7 7 0 110-14 7 7 0 010 14zm0-24L0 9.5l4.838 3.94A8 8 0 0112 9a8 8 0 017.162 4.44L24 9.5z"/>
                    </svg>
                    Scholar
                </a>
                <button class="btn btn-about" onclick='openModal(${JSON.stringify(paper).replace(/'/g, "&apos;")})'>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/>
                        <path d="M12 16v-4M12 8h.01"/>
                    </svg>
                    About
                </button>
            </div>
        </div>
    `;
}

// Format authors
function formatAuthors(authors, max = 3) {
    const authorList = authors.split(' and ').map(a => a.trim());
    if (authorList.length > max) {
        return authorList.slice(0, max).join(', ') + ', et al.';
    }
    return authorList.join(', ');
}

// Open modal with paper details
function openModal(paper) {
    document.getElementById('modal-title').textContent = paper.title;
    document.getElementById('modal-authors').textContent = formatAuthors(paper.authors, 100);
    document.getElementById('modal-year').textContent = paper.year;
    document.getElementById('modal-venue').textContent = paper.venue || '';
    document.getElementById('modal-abstract').textContent = paper.abstract || 'No abstract available.';
    document.getElementById('modal-bibtex').textContent = paper.bibtex || 'No BibTeX available.';

    document.getElementById('paper-modal').classList.add('active');
    document.body.style.overflow = 'hidden';
}

// Close modal
function closeModal() {
    document.getElementById('paper-modal').classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Close modal on outside click
document.getElementById('paper-modal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeModal();
    }
});

// Close modal on escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeModal();
    }
});

// Update stats
function updateStats() {
    document.getElementById('total-papers').textContent = allPapers;
    document.getElementById('total-categories').textContent = allCategories;
}

// Set current date
document.getElementById('current-date').textContent = new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
});

// Load taxonomies on page load
loadTaxonomies();
