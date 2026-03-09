"""
Image Generation Module
Generates AI-powered product images for WordPress posts
"""

import os
import random
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime


class ImageGenerator:
    """Generates product images using AI"""

    def __init__(self, openai_api_key: str, assets_dir: str = None):
        self.openai_api_key = openai_api_key
        self.assets_dir = Path(assets_dir) if assets_dir else Path(__file__).parent.parent / 'assets'
        self.assets_dir.mkdir(parents=True, exist_ok=True)

    def generate_product_image(self, product: str, keyword: str) -> Optional[Dict]:
        """Generate a product image using DALL-E"""

        if not self.openai_api_key:
            # Return placeholder if no API key
            return self._get_placeholder_image(product, keyword)

        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_api_key)

            # Create prompt for product image
            prompt = self._create_image_prompt(product)

            # Generate image
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )

            # Get image URL
            image_url = response.data[0].url

            # Download and save image
            return self._download_and_save_image(image_url, product, keyword)

        except Exception as e:
            print(f"Error generating image: {e}")
            return self._get_placeholder_image(product, keyword)

    def _create_image_prompt(self, product: str) -> str:
        """Create detailed prompt for product image generation"""

        prompts = [
            f"Professional industrial product photography of {product}, clean white background, studio lighting, high resolution, commercial use, detailed view showing texture and quality",
            f"High-quality product image of {product}, modern commercial photography, neutral background, professional lighting, showcase detailed features, 4k quality",
            f"Premium {product} for industrial use, clean studio shot, white background, professional commercial photography, highlighting durability and quality"
        ]

        return random.choice(prompts)

    def _download_and_save_image(self, image_url: str, product: str, keyword: str) -> Dict:
        """Download image from URL and save to assets folder"""

        import requests

        try:
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_product = "".join(c for c in product if c.isalnum() or c in ['-', '_'])
            filename = f"{safe_product}_{timestamp}.png"
            filepath = self.assets_dir / filename

            # Download image
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()

            # Save image
            with open(filepath, 'wb') as f:
                f.write(response.content)

            return {
                'filename': filename,
                'filepath': str(filepath),
                'alt_text': keyword,
                'caption': f"High-quality {keyword} from China manufacturer"
            }

        except Exception as e:
            print(f"Error downloading image: {e}")
            return self._get_placeholder_image(product, keyword)

    def _get_placeholder_image(self, product: str, keyword: str) -> Dict:
        """Generate placeholder image data when API is not available"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"placeholder_{timestamp}.jpg"
        filepath = self.assets_dir / filename

        # Create a simple placeholder using PIL
        try:
            from PIL import Image, ImageDraw, ImageFont

            # Create image
            img = Image.new('RGB', (800, 600), color=(240, 240, 245))
            draw = ImageDraw.Draw(img)

            # Add text
            text = f"Product Image: {keyword.title()}"
            # Simple text drawing (using default font)
            draw.text((50, 280), text, fill=(100, 100, 100))

            # Save image
            img.save(filepath, 'JPEG', quality=85)

            return {
                'filename': filename,
                'filepath': str(filepath),
                'alt_text': keyword,
                'caption': f"Professional {keyword} from China"
            }

        except Exception as e:
            print(f"Error creating placeholder: {e}")
            return {
                'filename': 'no_image.jpg',
                'filepath': None,
                'alt_text': keyword,
                'caption': f"Professional {keyword} from China"
            }

    def generate_gallery_images(self, product: str, count: int = 3) -> list:
        """Generate multiple images for product gallery"""

        images = []

        # Generate main image
        main_image = self.generate_product_image(product, product)
        if main_image:
            images.append(main_image)

        # Generate additional views if API available
        if self.openai_api_key and count > 1:
            variations = [
                f"{product} detail view",
                f"{product} application example",
                f"{product} in use"
            ]

            for i in range(min(count - 1, len(variations))):
                img = self.generate_product_image(variations[i], product)
                if img:
                    images.append(img)

        return images


def generate_product_image(product: str, keyword: str, config: Dict) -> Dict:
    """Helper function to generate product image"""
    generator = ImageGenerator(
        openai_api_key=config.get('openai_api_key', ''),
        assets_dir=config.get('assets_dir')
    )
    return generator.generate_product_image(product, keyword)
