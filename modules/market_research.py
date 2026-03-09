"""
Market Research Module
Discovers high-margin China export products for content generation
"""

import random
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class MarketResearch:
    """Market research for high-margin China export products"""

    def __init__(self, existing_products: List[Dict], high_margin_products: List[str]):
        self.existing_products = existing_products
        self.high_margin_products = high_margin_products
        self.history_file = Path(__file__).parent.parent / 'data' / 'history.json'
        self._ensure_history_file()

    def _ensure_history_file(self):
        """Ensure history file exists"""
        if not self.history_file.exists():
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.history_file, 'w') as f:
                json.dump({
                    'published_topics': [],
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)

    def _load_history(self) -> Dict:
        """Load publishing history"""
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {'published_topics': [], 'last_updated': datetime.now().isoformat()}

    def _save_history(self, history: Dict):
        """Save publishing history"""
        history['last_updated'] = datetime.now().isoformat()
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)

    def get_existing_product_topics(self, count: int = 15) -> List[Dict]:
        """Generate topics from existing products with variations"""
        topics = []
        history = self._load_history()
        published = set(history.get('published_topics', []))

        # Create variations for each existing product
        variations = [
            '{product} for industrial warehouse',
            '{product} for commercial building',
            '{product} for residential garage',
            '{product} for outdoor application',
            '{product} for heavy duty use',
            '{product} for automotive workshop',
            '{product} for manufacturing facility',
            '{product} for logistics center',
            '{product} for construction site',
            '{product} for parking lot',
            '{product} wholesale supplier',
            '{product} manufacturer direct',
            '{product} factory price',
            '{product} customization service',
            '{product} installation guide'
        ]

        # Shuffle products for variety
        shuffled_products = self.existing_products.copy()
        random.shuffle(shuffled_products)

        for product_data in shuffled_products:
            if len(topics) >= count:
                break

            # Handle both dict and string formats for compatibility
            if isinstance(product_data, dict):
                product_name = product_data['name']
                category_id = product_data.get('category_id')
            else:
                product_name = product_data
                category_id = None

            # Generate topic with variation
            variation = random.choice(variations)
            topic_title = variation.format(product=product_name.title())

            # Create unique slug
            base_slug = product_name.lower().replace(' ', '-')
            slug = f"{base_slug}-{random.randint(1000, 9999)}"

            if topic_title not in published:
                topics.append({
                    'type': 'existing',
                    'product': product_name,
                    'title': topic_title,
                    'slug': slug,
                    'keyword': product_name.lower(),
                    'category_id': category_id
                })

                # Update history
                history['published_topics'].append(topic_title)
                self._save_history(history)

        return topics[:count]

    def get_new_product_topics(self, count: int = 15) -> List[Dict]:
        """Generate topics from new high-margin products"""
        topics = []
        history = self._load_history()
        published = set(history.get('published_topics', []))

        # Shuffle products for variety
        shuffled_products = self.high_margin_products.copy()
        random.shuffle(shuffled_products)

        for product in shuffled_products:
            if len(topics) >= count:
                break

            # Generate compelling title with power words
            power_words = ['Premium', 'Industrial', 'Professional', 'Commercial',
                          'High-Performance', 'Heavy-Duty', 'Best', 'Top']

            # Create variations
            variations = [
                f"{random.choice(power_words)} {product.title()} for Global Export",
                f"{product.title()}: China Manufacturer Direct Supply",
                f"Wholesale {product.title()} - Factory Price Export",
                f"{product.title()} for International Market Distribution",
                f"High-Quality {product.title()} - B2B Export Solutions",
                f"Custom {product.title()} Manufacturing & Export",
                f"Professional {product.title()} Supplier from China",
                f"Commercial {product.title()} - Global Shipping Available"
            ]

            topic_title = random.choice(variations)

            # Create unique slug
            base_slug = product.lower().replace(' ', '-')
            slug = f"{base_slug}-china-export-{random.randint(100, 999)}"

            if topic_title not in published:
                topics.append({
                    'type': 'new',
                    'product': product,
                    'title': topic_title,
                    'slug': slug,
                    'keyword': product.lower(),
                    'category': self._categorize_product(product)
                })

                # Update history
                history['published_topics'].append(topic_title)
                self._save_history(history)

        return topics[:count]

    def _categorize_product(self, product: str) -> str:
        """Categorize product for WordPress category creation"""
        product_lower = product.lower()

        categories = {
            'industrial_equipment': ['laser cutting', 'cnc router', 'robot arm', 'forklift', 'hydraulic press'],
            'energy_storage': ['lithium battery', 'solar panel', 'wind turbine', 'energy storage', 'ev charging'],
            'construction': ['prefab', 'steel structure', 'bridge', 'acoustic panel', 'fireproof door'],
            'agricultural': ['farming', 'drone', 'grain storage', 'irrigation', 'greenhouse'],
            'medical': ['hospital', 'medical imaging', 'diagnostic', 'dental equipment'],
            'packaging': ['packaging machine', 'conveyor', 'warehouse', 'cold chain', 'container'],
            'flooring': ['vinyl plank', 'rubber flooring', 'carpet tile', 'artificial grass', 'sports floor'],
            'safety': ['explosion proof', 'safety shower', 'fall protection', 'dust collection', 'soundproof']
        }

        for category, keywords in categories.items():
            if any(kw in product_lower for kw in keywords):
                return category

        return 'general_export'

    def get_trending_topics(self, count: int = 5) -> List[Dict]:
        """Get trending topics based on current events"""
        # Current trending topics for industrial/B2B
        trending = [
            {
                'title': 'Sustainable Building Materials for Green Construction 2024',
                'keyword': 'sustainable building materials',
                'category': 'construction'
            },
            {
                'title': 'EV Infrastructure Solutions for Commercial Properties',
                'keyword': 'ev infrastructure',
                'category': 'energy_storage'
            },
            {
                'title': 'Smart Warehouse Automation Systems for Logistics',
                'keyword': 'warehouse automation',
                'category': 'packaging'
            },
            {
                'title': 'Renewable Energy Storage Solutions for Industrial Use',
                'keyword': 'industrial energy storage',
                'category': 'energy_storage'
            },
            {
                'title': 'Industrial Automation Robotics for Manufacturing',
                'keyword': 'industrial automation',
                'category': 'industrial_equipment'
            }
        ]

        return random.sample(trending, min(count, len(trending)))

    def get_all_topics(self, existing_count: int = 15, new_count: int = 15) -> List[Dict]:
        """Get all topics for daily generation"""
        topics = []

        # Get existing product topics
        existing_topics = self.get_existing_product_topics(existing_count)
        topics.extend(existing_topics)

        # Get new product topics
        new_topics = self.get_new_product_topics(new_count)
        topics.extend(new_topics)

        # Shuffle all topics
        random.shuffle(topics)

        return topics
