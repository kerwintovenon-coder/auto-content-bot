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

    # Existing Products List
    EXISTING_PRODUCTS = [
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
