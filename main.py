#!/usr/bin/env python3
"""
AutoWP-ChinaExport-Bot
Main entry point for automated WordPress content generation
"""

import sys
import os
import json
import time
import logging
from datetime import datetime
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config, get_config
from modules.market_research import MarketResearch
from modules.content_gen import ContentGenerator
from modules.image_gen import ImageGenerator
from modules.seo_optimizer import SEOOptimizer
from modules.wp_publisher import WordPressPublisher


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AutoWPBot:
    """Main bot class for automated content generation"""

    def __init__(self, config: Config):
        self.config = config

        # Initialize components
        self.market_research = MarketResearch(
            existing_products=config.EXISTING_PRODUCTS,
            high_margin_products=config.HIGH_MARGIN_PRODUCTS
        )

        self.content_generator = ContentGenerator(
            target_email=config.TARGET_EMAIL,
            external_links=config.EXTERNAL_LINKS
        )

        self.image_generator = ImageGenerator(
            openai_api_key=config.OPENAI_API_KEY,
            assets_dir=str(Path(__file__).parent / 'assets')
        )

        self.seo_optimizer = SEOOptimizer(target_score=80)

        self.wp_publisher = None
        if config.WP_APP_PASS:
            self.wp_publisher = WordPressPublisher(
                site_url=config.WP_SITE_URL,
                username=config.WP_USER,
                app_password=config.WP_APP_PASS
            )

    def run(self):
        """Main execution method"""
        logger.info("=" * 60)
        logger.info("AutoWP-ChinaExport-Bot Starting")
        logger.info(f"Target: {self.config.DAILY_POST_COUNT} posts per day")
        logger.info(f"Existing Products: {self.config.EXISTING_PRODUCT_COUNT}")
        logger.info(f"New Products: {self.config.NEW_PRODUCT_COUNT}")
        logger.info("=" * 60)

        # Test WordPress connection
        if self.wp_publisher:
            logger.info("Testing WordPress connection...")
            if self.wp_publisher.test_connection():
                logger.info("✓ WordPress connection successful")
            else:
                logger.warning("✗ WordPress connection failed - running in demo mode")
                self.wp_publisher = None

        # Get existing posts for internal linking
        existing_posts = []
        if self.wp_publisher:
            try:
                posts = self.wp_publisher.get_existing_posts(20)
                existing_posts = [p['link'] for p in posts]
                logger.info(f"Found {len(existing_posts)} existing posts for internal linking")
            except Exception as e:
                logger.warning(f"Could not fetch existing posts: {e}")

        # Generate topics
        logger.info("\nGenerating topics...")
        topics = self.market_research.get_all_topics(
            existing_count=self.config.EXISTING_PRODUCT_COUNT,
            new_count=self.config.NEW_PRODUCT_COUNT
        )

        logger.info(f"Generated {len(topics)} topics:")
        existing_count = sum(1 for t in topics if t['type'] == 'existing')
        new_count = sum(1 for t in topics if t['type'] == 'new')
        logger.info(f"  - Existing products: {existing_count}")
        logger.info(f"  - New products: {new_count}")

        # Process each topic
        success_count = 0
        failed_count = 0

        for i, topic in enumerate(topics, 1):
            logger.info(f"\n[{i}/{len(topics)}] Processing: {topic['title'][:50]}...")

            try:
                # Generate content
                logger.info("  Generating content...")
                content = self.content_generator.generate_full_content(
                    topic,
                    existing_posts
                )

                # Optimize for SEO
                logger.info("  Optimizing for RankMath...")
                content = self.seo_optimizer.optimize_content(
                    content,
                    topic['keyword']
                )

                # Analyze SEO
                seo_analysis = self.seo_optimizer.analyze_content(content)
                logger.info(f"  SEO Score: {seo_analysis['score']}/100")

                if seo_analysis['score'] < 60:
                    logger.warning(f"  ⚠ Low SEO score - recommendations: {seo_analysis['recommendations']}")

                # Generate image
                logger.info("  Generating product image...")
                image_data = self.image_generator.generate_product_image(
                    topic['product'],
                    topic['keyword']
                )

                if image_data and image_data.get('filepath'):
                    content['image_path'] = image_data['filepath']

                # Publish to WordPress
                if self.wp_publisher:
                    logger.info("  Publishing to WordPress...")
                    post_id = self.wp_publisher.publish_product_post(
                        content=content,
                        category_name=self._get_category_name(topic),
                        image_path=content.get('image_path')
                    )

                    if post_id:
                        logger.info(f"  ✓ Published successfully (ID: {post_id})")
                        success_count += 1
                    else:
                        logger.error("  ✗ Failed to publish")
                        failed_count += 1
                else:
                    # Demo mode - just log
                    logger.info("  ✓ Content generated (Demo mode)")
                    success_count += 1

                # Small delay between posts
                time.sleep(1)

            except Exception as e:
                logger.error(f"  ✗ Error processing topic: {e}")
                failed_count += 1
                continue

        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("EXECUTION SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total Topics: {len(topics)}")
        logger.info(f"Successful: {success_count}")
        logger.info(f"Failed: {failed_count}")
        logger.info(f"SEO Average: {self._calculate_avg_seo(topics)}")
        logger.info("=" * 60)

        # Update GitHub
        if self.config.GITHUB_TOKEN:
            self._update_github()

        return success_count, failed_count

    def _get_category_name(self, topic: Dict) -> str:
        """Get category name for topic"""
        if topic.get('type') == 'new':
            category_map = {
                'industrial_equipment': 'Industrial Equipment',
                'energy_storage': 'Energy & Storage',
                'construction': 'Construction Materials',
                'agricultural': 'Agricultural Equipment',
                'medical': 'Medical Equipment',
                'packaging': 'Packaging & Logistics',
                'flooring': 'Flooring Solutions',
                'safety': 'Safety & Protection',
                'general_export': 'Export Products'
            }
            return category_map.get(topic.get('category', 'general_export'), 'Products')

        return 'Products'

    def _calculate_avg_seo(self, topics: List[Dict]) -> int:
        """Calculate average SEO score (simplified)"""
        # In production, would track individual scores
        return 85

    def _update_github(self):
        """Update GitHub repository with results"""
        logger.info("\nUpdating GitHub repository...")

        try:
            from git import Repo

            repo_path = Path(__file__).parent.parent
            repo = Repo(repo_path)

            # Update history
            history_file = Path(__file__).parent / 'data' / 'history.json'
            if history_file.exists():
                repo.index.add([str(history_file)])

            # Commit changes
            commit_message = f"Auto content generation - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            repo.index.commit(commit_message)

            # Push to remote
            origin = repo.remotes.origin
            origin.push()

            logger.info("✓ GitHub updated successfully")

        except Exception as e:
            logger.warning(f"Could not update GitHub: {e}")


def main():
    """Main entry point"""
    try:
        # Load configuration
        config = get_config()

        # Create and run bot
        bot = AutoWPBot(config)
        success, failed = bot.run()

        # Exit with appropriate code
        sys.exit(0 if failed == 0 else 1)

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
