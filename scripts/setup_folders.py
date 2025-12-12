#!/usr/bin/env python3
"""
Setup citation folder structure based on taxonomy categories.
Run this once to create all category folders.
"""

from pathlib import Path

# Category definitions (must match build_taxonomies.py)
CATEGORIES = {
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

def main():
    project_root = Path(__file__).parent.parent
    citations_dir = project_root / 'citations'

    print("=" * 60)
    print("📁 SETTING UP CITATION FOLDERS")
    print("=" * 60)
    print(f"\nBase directory: {citations_dir}\n")

    # Create citations directory if it doesn't exist
    citations_dir.mkdir(exist_ok=True)

    # Create each category folder
    created = 0
    existing = 0

    for folder_name, info in CATEGORIES.items():
        folder_path = citations_dir / folder_name

        if folder_path.exists():
            print(f"  ✓ {folder_name:30s} (already exists)")
            existing += 1
        else:
            folder_path.mkdir(parents=True)
            print(f"  ✨ {folder_name:30s} (created)")
            created += 1

    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"  Created:  {created} folders")
    print(f"  Existing: {existing} folders")
    print(f"  Total:    {len(CATEGORIES)} folders")
    print("=" * 60)

    print("\n💡 Next steps:")
    print("  1. Save .bib files to appropriate folders:")
    for folder_name, info in list(CATEGORIES.items())[:3]:
        print(f"     - citations/{folder_name}/<paper>.bib")
    print("     - ...")
    print(f"\n  2. Run: python scripts/build_taxonomies.py")
    print(f"  3. Open index.html in a browser")

    # Print category reference
    print("\n" + "=" * 60)
    print("📚 CATEGORY REFERENCE")
    print("=" * 60)
    for folder_name, info in CATEGORIES.items():
        print(f"\n{folder_name}/")
        print(f"  {info['name']}")
        print(f"  → {info['description']}")

if __name__ == '__main__':
    main()
