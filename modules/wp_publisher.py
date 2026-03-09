"""
WordPress Publisher Module
Publishes content to WordPress via REST API
"""

import base64
import json
import requests
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path


class WordPressPublisher:
    """Publishes content to WordPress using REST API"""

    def __init__(self, site_url: str, username: str, app_password: str):
        self.site_url = site_url.rstrip('/')
        self.username = username
        self.app_password = app_password

        # Setup authentication
        self.auth = base64.b64encode(f"{username}:{app_password}".encode()).decode()
        self.headers = {
            'Authorization': f'Basic {self.auth}',
            'Content-Type': 'application/json'
        }

        self.api_url = f"{self.site_url}/wp-json/wp/v2"

    def test_connection(self) -> bool:
        """Test WordPress connection"""
        try:
            response = requests.get(
                f"{self.api_url}/users/me",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

    def get_categories(self) -> List[Dict]:
        """Get existing categories"""
        try:
            response = requests.get(
                f"{self.api_url}/categories",
                headers=self.headers,
                params={'per_page': 100},
                timeout=10
            )

            if response.status_code == 200:
                return response.json()
            return []

        except Exception as e:
            print(f"Error getting categories: {e}")
            return []

    def create_category(self, name: str, description: str = '') -> Optional[int]:
        """Create new category and return ID"""
        try:
            response = requests.post(
                f"{self.api_url}/categories",
                headers=self.headers,
                json={
                    'name': name,
                    'description': description,
                    'slug': name.lower().replace(' ', '-')
                },
                timeout=10
            )

            if response.status_code == 201:
                return response.json()['id']
            elif response.status_code == 400:
                # Category might already exist, try to find it
                categories = self.get_categories()
                for cat in categories:
                    if cat['name'].lower() == name.lower():
                        return cat['id']

            return None

        except Exception as e:
            print(f"Error creating category: {e}")
            return None

    def get_tags(self) -> List[Dict]:
        """Get existing tags"""
        try:
            response = requests.get(
                f"{self.api_url}/tags",
                headers=self.headers,
                params={'per_page': 100},
                timeout=10
            )

            if response.status_code == 200:
                return response.json()
            return []

        except Exception as e:
            print(f"Error getting tags: {e}")
            return []

    def create_tag(self, name: str) -> Optional[int]:
        """Create new tag and return ID"""
        try:
            response = requests.post(
                f"{self.api_url}/tags",
                headers=self.headers,
                json={
                    'name': name,
                    'slug': name.lower().replace(' ', '-')
                },
                timeout=10
            )

            if response.status_code == 201:
                return response.json()['id']
            return None

        except Exception as e:
            print(f"Error creating tag: {e}")
            return None

    def upload_media(self, image_path: str, alt_text: str = '') -> Optional[Dict]:
        """Upload image to WordPress media library"""
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()

            # Determine mime type
            import mimetypes
            mime_type = mimetypes.guess_type(image_path)[0] or 'image/jpeg'

            # Prepare headers for media upload
            media_headers = {
                'Authorization': f'Basic {self.auth}',
                'Content-Disposition': f'attachment; filename={Path(image_path).name}'
            }

            response = requests.post(
                f"{self.api_url}/media",
                headers=media_headers,
                data=image_data,
                timeout=30
            )

            if response.status_code == 201:
                media = response.json()
                # Update alt text
                if alt_text:
                    requests.post(
                        f"{self.api_url}/media/{media['id']}",
                        headers=self.headers,
                        json={'alt_text': alt_text},
                        timeout=10
                    )

                return {
                    'id': media['id'],
                    'url': media['source_url'],
                    'alt': alt_text
                }

            return None

        except Exception as e:
            print(f"Error uploading media: {e}")
            return None

    def get_existing_posts(self, count: int = 20) -> List[Dict]:
        """Get existing posts for internal linking"""
        try:
            response = requests.get(
                f"{self.api_url}/posts",
                headers=self.headers,
                params={'per_page': count, 'status': 'publish'},
                timeout=10
            )

            if response.status_code == 200:
                return response.json()
            return []

        except Exception as e:
            print(f"Error getting posts: {e}")
            return []

    def create_post(self, content: Dict, category_ids: List[int] = None,
                   tag_ids: List[int] = None, featured_media: int = None,
                   status: str = 'publish') -> Optional[int]:
        """Create new post in WordPress"""

        try:
            # Build post data
            post_data = {
                'title': content['title'],
                'content': content['content'],
                'excerpt': content.get('excerpt', ''),
                'slug': content.get('slug', ''),
                'status': status,
                'meta': {
                    'rank_math_focus_keyword': content.get('keyword', ''),
                    'rank_math_description': content.get('meta_description', ''),
                    'rank_math_title': content.get('title', '')
                }
            }

            # Add category if provided
            if category_ids:
                post_data['categories'] = category_ids

            # Add tags if provided
            if tag_ids:
                post_data['tags'] = tag_ids

            # Add featured image if provided
            if featured_media:
                post_data['featured_media'] = featured_media

            # Create post
            response = requests.post(
                f"{self.api_url}/posts",
                headers=self.headers,
                json=post_data,
                timeout=30
            )

            if response.status_code == 201:
                post = response.json()
                print(f"Post created successfully: {post['link']}")
                return post['id']
            else:
                print(f"Error creating post: {response.status_code}")
                print(response.text)
                return None

        except Exception as e:
            print(f"Error creating post: {e}")
            return None

    def update_post_meta(self, post_id: int, meta: Dict) -> bool:
        """Update post meta fields for RankMath"""
        try:
            response = requests.post(
                f"{self.api_url}/posts/{post_id}",
                headers=self.headers,
                json={'meta': meta},
                timeout=10
            )

            return response.status_code == 200

        except Exception as e:
            print(f"Error updating meta: {e}")
            return False

    def publish_product_post(self, content: Dict, category_name: str = 'Products',
                           image_path: str = None) -> Optional[int]:
        """Publish a complete product post with all elements"""

        # Get or create category
        category_id = self._get_or_create_category(category_name)

        # Upload featured image if provided
        featured_media = None
        if image_path and Path(image_path).exists():
            media = self.upload_media(image_path, content.get('keyword', ''))
            if media:
                featured_media = media['id']

        # Create post
        post_id = self.create_post(
            content=content,
            category_ids=[category_id] if category_id else None,
            featured_media=featured_media,
            status='publish'
        )

        return post_id

    def _get_or_create_category(self, name: str) -> Optional[int]:
        """Get existing category or create new one"""
        categories = self.get_categories()

        # Check if category exists
        for cat in categories:
            if cat['name'].lower() == name.lower():
                return cat['id']

        # Create new category
        return self.create_category(name)


def publish_to_wordpress(content: Dict, config: Dict) -> Optional[int]:
    """Helper function to publish content to WordPress"""

    publisher = WordPressPublisher(
        site_url=config['wp_site_url'],
        username=config['wp_user'],
        app_password=config['wp_app_pass']
    )

    # Test connection
    if not publisher.test_connection():
        print("Failed to connect to WordPress")
        return None

    # Get existing posts for internal linking
    existing_posts = publisher.get_existing_posts(20)

    # Publish post
    return publisher.publish_product_post(
        content=content,
        category_name=content.get('category', 'Products'),
        image_path=content.get('image_path')
    )
