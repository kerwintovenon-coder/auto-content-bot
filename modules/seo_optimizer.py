"""
SEO Optimizer Module
Optimizes content for RankMath SEO scoring (target: 80+)
"""

import re
from typing import Dict, List, Tuple


class SEOOptimizer:
    """Optimizes content for RankMath SEO scoring"""

    # Required elements for RankMath 80+
    REQUIRED_ELEMENTS = {
        'focus_keyword': True,
        'meta_description': True,
        'title_with_keyword': True,
        'slug_with_keyword': True,
        'content_length': 1000,  # Minimum words
        'keyword_density': (1.0, 2.5),  # Percentage range
        'headings_with_keyword': True,
        'image_with_alt': True,
        'external_links': 1,
        'internal_links': 1,
        'short_paragraphs': True,
        'conclusion': True
    }

    def __init__(self, target_score: int = 80):
        self.target_score = target_score

    def analyze_content(self, content: Dict) -> Dict:
        """Analyze content and return SEO score with recommendations"""

        analysis = {
            'score': 0,
            'max_score': 100,
            'passed': [],
            'failed': [],
            'recommendations': []
        }

        # Check focus keyword in title
        if self._keyword_in_title(content.get('title', ''), content.get('keyword', '')):
            analysis['passed'].append('Keyword in title')
            analysis['score'] += 10
        else:
            analysis['failed'].append('Keyword in title')
            analysis['recommendations'].append('Add focus keyword to the title')

        # Check meta description
        if self._has_meta_description(content.get('meta_description', '')):
            analysis['passed'].append('Meta description')
            analysis['score'] += 10
        else:
            analysis['failed'].append('Meta description')
            analysis['recommendations'].append('Add a meta description (150-160 characters)')

        # Check slug
        if self._keyword_in_slug(content.get('slug', ''), content.get('keyword', '')):
            analysis['passed'].append('Keyword in URL slug')
            analysis['score'] += 5
        else:
            analysis['failed'].append('Keyword in URL slug')
            analysis['recommendations'].append('Include keyword in URL slug')

        # Check content length
        content_length = len(content.get('content', '').split())
        if content_length >= self.REQUIRED_ELEMENTS['content_length']:
            analysis['passed'].append(f'Content length ({content_length} words)')
            analysis['score'] += 15
        else:
            analysis['failed'].append(f'Content length ({content_length} words)')
            analysis['recommendations'].append(f'Add more content (minimum {self.REQUIRED_ELEMENTS["content_length"]} words)')

        # Check keyword density
        density_info = self._check_keyword_density(
            content.get('content', ''),
            content.get('keyword', '')
        )
        if density_info['valid']:
            analysis['passed'].append(f'Keyword density ({density_info["density"]:.1f}%)')
            analysis['score'] += 15
        else:
            analysis['failed'].append(f'Keyword density ({density_info["density"]:.1f}%)')
            analysis['recommendations'].append(f'Adjust keyword density to {self.REQUIRED_ELEMENTS["keyword_density"][0]}-{self.REQUIRED_ELEMENTS["keyword_density"][1]}%')

        # Check headings
        if self._keyword_in_headings(content.get('content', ''), content.get('keyword', '')):
            analysis['passed'].append('Keyword in headings')
            analysis['score'] += 10
        else:
            analysis['failed'].append('Keyword in headings')
            analysis['recommendations'].append('Add focus keyword to at least one subheading (H2 or H3)')

        # Check images
        if self._has_images_with_alt(content.get('content', '')):
            analysis['passed'].append('Images with alt text')
            analysis['score'] += 10
        else:
            analysis['failed'].append('Images with alt text')
            analysis['recommendations'].append('Add at least one image with alt text containing keyword')

        # Check external links
        if len(content.get('external_links', [])) >= self.REQUIRED_ELEMENTS['external_links']:
            analysis['passed'].append('External links')
            analysis['score'] += 10
        else:
            analysis['failed'].append('External links')
            analysis['recommendations'].append('Add at least one external link to authoritative source')

        # Check internal links
        if len(content.get('internal_links', [])) >= self.REQUIRED_ELEMENTS['internal_links']:
            analysis['passed'].append('Internal links')
            analysis['score'] += 10
        else:
            analysis['failed'].append('Internal links')
            analysis['recommendations'].append('Add internal links to related posts')

        # Check short paragraphs
        if self._has_short_paragraphs(content.get('content', '')):
            analysis['passed'].append('Short paragraphs')
            analysis['score'] += 5
        else:
            analysis['failed'].append('Short paragraphs')
            analysis['recommendations'].append('Use shorter paragraphs (max 3-4 sentences)')

        return analysis

    def _keyword_in_title(self, title: str, keyword: str) -> bool:
        """Check if keyword appears in title"""
        if not title or not keyword:
            return False
        return keyword.lower() in title.lower()

    def _has_meta_description(self, meta_desc: str) -> bool:
        """Check if meta description exists and is proper length"""
        if not meta_desc:
            return False
        return 120 <= len(meta_desc) <= 160

    def _keyword_in_slug(self, slug: str, keyword: str) -> bool:
        """Check if keyword appears in URL slug"""
        if not slug or not keyword:
            return False
        keyword_slug = keyword.lower().replace(' ', '-')
        return keyword_slug in slug.lower()

    def _check_keyword_density(self, content: str, keyword: str) -> Dict:
        """Check keyword density in content"""
        if not content or not keyword:
            return {'valid': False, 'density': 0}

        words = content.lower().split()
        keyword_lower = keyword.lower()

        keyword_count = sum(1 for word in words if keyword_lower in word)
        total_words = len(words)

        if total_words == 0:
            return {'valid': False, 'density': 0}

        density = (keyword_count / total_words) * 100
        min_density, max_density = self.REQUIRED_ELEMENTS['keyword_density']

        return {
            'valid': min_density <= density <= max_density,
            'density': density
        }

    def _keyword_in_headings(self, content: str, keyword: str) -> bool:
        """Check if keyword appears in headings"""
        if not content or not keyword:
            return False

        # Find all headings (h2, h3, h4)
        heading_pattern = r'<h[2-4][^>]*>(.*?)</h[2-4]>'
        headings = re.findall(heading_pattern, content, re.IGNORECASE)

        keyword_lower = keyword.lower()
        return any(keyword_lower in heading.lower() for heading in headings)

    def _has_images_with_alt(self, content: str) -> bool:
        """Check if content has images with alt text"""
        if not content:
            return False

        # Check for img tags with alt attribute
        img_pattern = r'<img[^>]+alt=["\']([^"\']+)["\'][^>]*>'
        images_with_alt = re.findall(img_pattern, content, re.IGNORECASE)

        return len(images_with_alt) > 0

    def _has_short_paragraphs(self, content: str) -> bool:
        """Check if paragraphs are reasonably short"""
        if not content:
            return False

        # Split content into paragraphs
        paragraphs = re.split(r'\n\s*\n', content)

        # Check if most paragraphs are short (less than 150 words)
        short_count = sum(1 for p in paragraphs if len(p.split()) <= 150)

        return short_count >= len(paragraphs) * 0.7

    def optimize_content(self, content: Dict, keyword: str) -> Dict:
        """Optimize content to meet SEO requirements"""

        optimized = content.copy()

        # Ensure keyword is in title
        if keyword.lower() not in optimized.get('title', '').lower():
            optimized['title'] = f"{keyword.title()}: {optimized.get('title', '')[:50]}"

        # Ensure meta description exists
        if not optimized.get('meta_description'):
            optimized['meta_description'] = f"Professional {keyword} from China. Factory direct pricing, ISO certified, global export. Contact {optimized.get('email', 'us')} for quotes."

        # Ensure slug contains keyword
        keyword_slug = keyword.lower().replace(' ', '-')
        if keyword_slug not in optimized.get('slug', '').lower():
            optimized['slug'] = f"{keyword_slug}-{optimized.get('slug', '')[:20]}"

        # Add alt text to images if missing
        content = optimized.get('content', '')
        if 'alt=' not in content.lower():
            # Add image with alt text at the beginning
            image_html = f'<img src="product-image.jpg" alt="{keyword}" title="{keyword}" />\n\n'
            optimized['content'] = image_html + content

        # Add conclusion if missing
        if 'conclusion' not in content.lower() and 'contact' not in content.lower():
            optimized['content'] += f'\n\n<h2>Conclusion</h2>\n<p>We are your trusted partner for {keyword} from China. Contact us at {optimized.get("email", "info@milgrp.com")} for competitive pricing and quality assurance.</p>'

        return optimized

    def get_rankmath_schema(self, content: Dict) -> Dict:
        """Generate RankMath JSON-LD schema"""

        keyword = content.get('keyword', '')
        title = content.get('title', '')

        schema = {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": title,
            "description": content.get('meta_description', ''),
            "brand": {
                "@type": "Brand",
                "name": "MILGRP"
            },
            "manufacturer": {
                "@type": "Organization",
                "name": "China Manufacturer",
                "location": "            "keywords":China"
            },
 keyword,
            "offers": {
                "@type": "Offer",
                "priceCurrency": "USD",
                "price": "Contact for pricing",
                "availability": "https://schema.org/InStock",
                "seller": {
                    "@type": "Organization",
                    "name": "MILGRP"
                }
            }
        }

        return schema


def analyze_seo(content: Dict) -> Dict:
    """Helper function to analyze SEO"""
    optimizer = SEOOptimizer(target_score=80)
    return optimizer.analyze_content(content)


def optimize_for_rankmath(content: Dict, keyword: str) -> Dict:
    """Helper function to optimize content"""
    optimizer = SEOOptimizer(target_score=80)
    return optimizer.optimize_content(content, keyword)
