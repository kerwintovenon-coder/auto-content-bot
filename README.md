# AutoWP-ChinaExport-Bot
# WordPress Automated Content Generation System
# For milgrp.com - Daily 30 Posts Generation

## Project Overview
This system automatically generates and publishes SEO-optimized product content to WordPress.
- 15 posts for existing products (garage floor, pvc flooring, etc.)
- 15 posts for new high-margin China export products
- RankMath optimized (target: 80+ score)

## Directory Structure
```
autowp-bot/
├── main.py                 # Entry point
├── config.py               # Configuration
├── .env                    # Environment variables
├── requirements.txt        # Dependencies
├── modules/
│   ├── __init__.py
│   ├── market_research.py  # High-margin product discovery
│   ├── content_gen.py      # SEO content generation
│   ├── image_gen.py        # AI image generation
│   ├── seo_optimizer.py    # RankMath optimization
│   └── wp_publisher.py     # WordPress publisher
├── data/
│   └── history.json        # Publishing history
└── assets/                 # Generated images
```

## Setup
1. Install dependencies: pip install -r requirements.txt
2. Configure .env file with credentials
3. Run: python main.py

## Features
- Automated market research for trending products
- AI-powered content generation with SEO optimization
- Image generation for products
- WordPress REST API integration
- GitHub version control
- RankMath score optimization

## Security Note
Never commit .env file or expose credentials!
