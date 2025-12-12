#!/usr/bin/env python3
"""
Build taxonomy JSON files from BibTeX citations.
Reads abstracts directly from BibTeX entries.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict

# Category metadata
CATEGORY_INFO = {
    'surveys': {
        'name': 'Surveys and Bibliometric Analyses',
        'description': 'Literature and systematic reviews of long-tailed learning in healthcare'
    },
    'data-balancing': {
        'name': 'Data Balancing',
        'description': 'Resampling and synthetic data generation techniques for addressing class imbalance'
    },
    'neural-architecture': {
        'name': 'Neural Architecture',
        'description': 'Specialized network designs and architectural modifications for imbalanced data'
    },
    'feature-enrichment': {
        'name': 'Feature Enrichment',
        'description': 'Representation learning to produce more discriminative embeddings for minority classes'
    },
    'logits-adjustment': {
        'name': 'Logits Adjustment',
        'description': 'Modify classifier outputs to compensate for class frequency disparities'
    },
    'loss-functions': {
        'name': 'Loss Functions',
        'description': 'Loss function design for class-imbalanced learning'
    },
    'foundation-models': {
        'name': 'Foundation Models',
        'description': 'Addressing long-tailed distributions through transfer learning and efficient adaptation.'
    },
    'multimodality': {
        'name': 'Multi-modality',
        'description': 'Multi-modal learning approaches addressing missing modalities and class imbalance'
    },
    'fairness': {
        'name': 'Fairness, Bias, and Health Equity',
        'description': 'Methods addressing demographic imbalances and algorithmic fairness in healthcare'
    },
    'rare-disease': {
        'name': 'Rare Disease and Epidemiological Modeling',
        'description': 'Specialized approaches for extremely rare conditions and few-shot medical scenarios'
    }
}

def parse_bibtex_entry(bib_content: str) -> Dict[str, str]:
    """Parse a single BibTeX entry and extract key fields"""
    entry = {
        'id': '',
        'title': '',
        'authors': '',
        'year': '',
        'venue': '',
        'abstract': '',
        'bibtex': bib_content.strip()
    }

    # Extract entry type and ID
    match = re.match(r'^@(\w+)\{([^,]+),', bib_content)
    if match:
        entry['id'] = match.group(2).strip()

    # Extract title
    title_match = re.search(r'title\s*=\s*\{([^}]+)\}', bib_content, re.IGNORECASE)
    if title_match:
        entry['title'] = title_match.group(1).strip()

    # Extract authors
    author_match = re.search(r'author\s*=\s*\{([^}]+)\}', bib_content, re.IGNORECASE)
    if author_match:
        authors_raw = author_match.group(1).strip()
        entry['authors'] = authors_raw

    # Extract year
    year_match = re.search(r'year\s*=\s*\{?(\d{4})\}?', bib_content, re.IGNORECASE)
    if year_match:
        entry['year'] = year_match.group(1)

    # Extract venue (journal or booktitle)
    journal_match = re.search(r'journal\s*=\s*\{([^}]+)\}', bib_content, re.IGNORECASE)
    booktitle_match = re.search(r'booktitle\s*=\s*\{([^}]+)\}', bib_content, re.IGNORECASE)

    if journal_match:
        entry['venue'] = journal_match.group(1).strip()
    elif booktitle_match:
        entry['venue'] = booktitle_match.group(1).strip()

    # Extract abstract
    abstract_match = re.search(r'abstract\s*=\s*\{([^}]+)\}', bib_content, re.IGNORECASE | re.DOTALL)
    if abstract_match:
        entry['abstract'] = abstract_match.group(1).strip()
    else:
        entry['abstract'] = "Abstract not available."

    return entry

def process_category(category_folder: Path) -> Dict:
    """Process all .bib files in a category folder"""
    category_name = category_folder.name
    category_data = CATEGORY_INFO.get(category_name, {
        'name': category_name.replace('-', ' ').title(),
        'description': ''
    })

    papers = []

    # Read all .bib files
    bib_files = sorted(category_folder.glob('*.bib'))

    print(f"\n📂 Processing {category_data['name']} ({len(bib_files)} papers)")

    for bib_file in bib_files:
        with open(bib_file, 'r', encoding='utf-8') as f:
            bib_content = f.read()

        entry = parse_bibtex_entry(bib_content)
        papers.append(entry)

    return {
        'category': category_data['name'],
        'description': category_data['description'],
        'papers': papers
    }

def build_all_taxonomies(citations_dir: Path, output_dir: Path):
    """Build all taxonomy JSON files from citation folders"""
    citations_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    stats = {}

    # Process each category folder
    for category_folder in sorted(citations_dir.iterdir()):
        if category_folder.is_dir() and category_folder.name in CATEGORY_INFO:
            taxonomy = process_category(category_folder)

            # Save JSON file
            output_file = output_dir / f"{category_folder.name}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(taxonomy, f, indent=2, ensure_ascii=False)

            stats[category_folder.name] = len(taxonomy['papers'])
            print(f"  ✓ Saved {output_file.name}")

    return stats

def main():
    # Paths
    project_root = Path(__file__).parent.parent
    citations_dir = project_root / 'citations'
    output_dir = project_root / 'taxonomies'

    print("="*60)
    print("🏗️  BUILDING TAXONOMY DATABASE")
    print("="*60)
    print("\n📖 Reading abstracts from BibTeX entries...")

    # Build taxonomies
    stats = build_all_taxonomies(citations_dir, output_dir)

    # Print summary
    print("\n" + "="*60)
    print("📊 BUILD SUMMARY")
    print("="*60)
    for category, count in sorted(stats.items()):
        print(f"  {category:30s} {count:3d} papers")
    print("="*60)
    print(f"  {'TOTAL':30s} {sum(stats.values()):3d} papers")
    print("="*60)

    print(f"\n✅ Taxonomy files saved to: {output_dir}/")
    print("\n💡 Tip: You can now add new papers by:")
    print("   1. Saving a .bib file to citations/<category>/")
    print("   2. Running: python scripts/build_taxonomies.py")
    print("   3. Refreshing the website")

if __name__ == '__main__':
    main()
