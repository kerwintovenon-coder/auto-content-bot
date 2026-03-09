"""
AutoWP-ChinaExport-Bot Configuration Module
Loads environment variables and provides configuration settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)


class Config:
    """Configuration class for AutoWP Bot"""

    # WordPress Configuration
    WP_SITE_URL = os.getenv('WP_SITE_URL', 'https://milgrp.com')
    WP_USER = os.getenv('WP_USER', 'user')
    WP_APP_PASS = os.getenv('WP_APP_PASS', '')
    WP_EMAIL = os.getenv('WP_EMAIL', 'info@milgrp.com')

    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

    # GitHub Configuration
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
    GITHUB_REPO = os.getenv('GITHUB_REPO', 'kerwintovenon-coder/auto-content-bot')

    # Target Configuration
    TARGET_EMAIL = os.getenv('TARGET_EMAIL', 'info@milgrp.com')
    DAILY_POST_COUNT = int(os.getenv('DAILY_POST_COUNT', '30'))
    EXISTING_PRODUCT_COUNT = int(os.getenv('EXISTING_PRODUCT_COUNT', '15'))
    NEW_PRODUCT_COUNT = int(os.getenv('NEW_PRODUCT_COUNT', '15'))

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # Existing Products with WordPress Category IDs
    # These IDs are from milgrp.com WordPress installation
    EXISTING_PRODUCTS = [
        {'name': 'garage floor', 'category_id': 28, 'slug': 'garage-floor-tiles'},
        {'name': 'pvc flooring', 'category_id': 103, 'slug': 'pvc-flooring-roll'},
        {'name': 'anti-slip mat', 'category_id': 96, 'slug': 'anti-slip-mats'},
        {'name': 'oil absorbent', 'category_id': 155, 'slug': 'oil-absorbent-mats'},
        {'name': 'ground system', 'category_id': 97, 'slug': 'workshop-floors'},
        {'name': 'container house', 'category_id': 182, 'slug': 'container-houses'},
        {'name': 'modular space', 'category_id': 181, 'slug': 'modular-space'},
        {'name': 'hesco barrier', 'category_id': 205, 'slug': 'defensive-barrier'},
        {'name': 'flood barrier', 'category_id': 204, 'slug': 'flood-control-barrier'}
    ]

    # Legacy list for compatibility
    EXISTING_PRODUCT_NAMES = [
        'garage floor',
        'pvc flooring',
        'anti-slip mat',
        'oil absorbent',
        'ground system',
        'container house',
        'modular space',
        'hesco barrier',
        'flood barrier'
    ]

    # High Margin China Export Products (Pre-researched)
    HIGH_MARGIN_PRODUCTS = [
        # Industrial Equipment
        'laser cutting machine',
        'cnc router',
        'industrial robot arm',
        'electric forklift',
        'hydraulic press',

        # Energy & Storage
        'lithium battery storage',
        'solar panel system',
        'wind turbine generator',
        'energy storage battery',
        'EV charging station',

        # Construction Materials
        'prefab modular building',
        'steel structure warehouse',
        'temporary bridge system',
        'acoustic panel',
        'fireproof door',

        # Agricultural Equipment
        'vertical farming system',
        'agricultural drone',
        'grain storage silo',
        'irrigation system',
        'greenhouse structure',

        # Medical Equipment
        'hospital bed',
        'medical imaging device',
        'diagnostic equipment',
        'disposable medical supplies',
        'dental equipment',

        # Packaging & Logistics
        'automatic packaging machine',
        'conveyor belt system',
        'warehouse racking',
        'cold chain container',
        'shipping container modifier',

        # Textiles & Flooring
        'luxury vinyl plank',
        'rubber flooring tile',
        'carpet tile',
        'artificial grass',
        'sports floor coating',

        # Safety & Protection
        'explosion proof equipment',
        'industrial safety shower',
        'fall protection system',
        'dust collection system',
        'soundproof enclosure'
    ]

    # External Links for SEO
    EXTERNAL_LINKS = [
        'https://www.iso.org/standard/',
        'https://en.wikipedia.org/wiki/',
        'https://www.osha.gov/',
        'https://www.astm.org/',
        'https://www.ieee.org/',
    ]

    # Category mappings for new high-margin products
    # These categories will be created if they don't exist
    NEW_PRODUCT_CATEGORIES = {
        'industrial_equipment': {'name': 'Industrial Equipment', 'id': None},
        'energy_storage': {'name': 'Energy & Storage', 'id': None},
        'construction': {'name': 'Construction Materials', 'id': None},
        'agricultural': {'name': 'Agricultural Equipment', 'id': None},
        'medical': {'name': 'Medical Equipment', 'id': None},
        'packaging': {'name': 'Packaging & Logistics', 'id': None},
        'flooring': {'name': 'Flooring Solutions', 'id': None},
        'safety': {'name': 'Safety & Protection', 'id': None},
        'general_export': {'name': 'Export Products', 'id': None}
    }

    # Keyword to category mapping for new products
    KEYWORD_CATEGORY_MAP = {
        'laser cutting': 'industrial_equipment',
        'cnc router': 'industrial_equipment',
        'robot arm': 'industrial_equipment',
        'forklift': 'industrial_equipment',
        'hydraulic press': 'industrial_equipment',
        'lithium battery': 'energy_storage',
        'solar panel': 'energy_storage',
        'wind turbine': 'energy_storage',
        'energy storage': 'energy_storage',
        'ev charging': 'energy_storage',
        'prefab': 'construction',
        'steel structure': 'construction',
        'bridge': 'construction',
        'acoustic panel': 'construction',
        'fireproof door': 'construction',
        'farming': 'agricultural',
        'drone': 'agricultural',
        'grain storage': 'agricultural',
        'irrigation': 'agricultural',
        'greenhouse': 'agricultural',
        'hospital': 'medical',
        'medical imaging': 'medical',
        'diagnostic': 'medical',
        'dental': 'medical',
        'packaging': 'packaging',
        'conveyor': 'packaging',
        'warehouse': 'packaging',
        'cold chain': 'packaging',
        'container': 'packaging',
        'vinyl plank': 'flooring',
        'rubber flooring': 'flooring',
        'carpet tile': 'flooring',
        'artificial grass': 'flooring',
        'sports floor': 'flooring',
        'explosion proof': 'safety',
        'safety shower': 'safety',
        'fall protection': 'safety',
        'dust collection': 'safety',
        'soundproof': 'safety'
    }

    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required = [
            ('WP_SITE_URL', cls.WP_SITE_URL),
            ('WP_USER', cls.WP_USER),
            ('WP_APP_PASS', cls.WP_APP_PASS),
        ]

        missing = [name for name, value in required if not value]
        if missing:
            raise ValueError(f"Missing required config: {', '.join(missing)}")

        return True


def get_config():
    """Get validated configuration"""
    Config.validate()
    return Config
