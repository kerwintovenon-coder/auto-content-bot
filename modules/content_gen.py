"""
Content Generation Module
Generates SEO-optimized product content with all required elements
"""

import random
from typing import Dict, List, Optional
from datetime import datetime


class ContentGenerator:
    """Generates high-quality SEO content for products"""

    def __init__(self, target_email: str, external_links: List[str]):
        self.target_email = target_email
        self.external_links = external_links
        self.current_year = datetime.now().year

    def generate_product_specs_table(self, product: str, product_type: str) -> str:
        """Generate product specifications table HTML"""
        specs = self._get_product_specs(product, product_type)

        html = '''<div class="product-specifications">
<h2>Product Specifications</h2>
<table class="specs-table">
<tr><th>Specification</th><th>Details</th></tr>
'''
        for spec_name, spec_value in specs.items():
            html += f'<tr><td><strong>{spec_name}</strong></td><td>{spec_value}</td></tr>\n'

        html += '</table></div>'
        return html

    def _get_product_specs(self, product: str, product_type: str) -> Dict[str, str]:
        """Generate product-specific specifications"""
        base_specs = {
            'Material': self._get_material(product),
            'Origin': 'Made in China',
            'Certification': 'ISO 9001, CE, SGS',
            'MOQ': '1-50 Units',
            'Lead Time': '15-30 Days',
            'Payment Terms': 'T/T, L/C, Western Union',
            'Shipping': 'FOB, CIF, EXW Available',
            'Warranty': '1-2 Years Warranty'
        }

        # Add product-specific specs
        if 'floor' in product.lower() or 'mat' in product.lower():
            base_specs.update({
                'Thickness': '2mm - 10mm',
                'Size': 'Customizable',
                'Weight': '2-5 kg/m²',
                'Temperature Range': '-30°C to 80°C'
            })
        elif 'barrier' in product.lower() or 'flood' in product.lower():
            base_specs.update({
                'Height': '0.5m - 3m',
                'Length': '1m - 50m',
                'Load Capacity': '500-5000 kg/m²',
                'Installation': 'Quick Assembly'
            })
        elif 'container' in product.lower() or 'modular' in product.lower():
            base_specs.update({
                'Dimensions': '20ft / 40ft / Custom',
                'Steel Grade': 'Q235/Q345',
                'Wind Resistance': '120 km/h',
                'Earthquake Resistance': 'Grade 8'
            })

        return base_specs

    def _get_material(self, product: str) -> str:
        """Determine material based on product"""
        product_lower = product.lower()
        if 'pvc' in product_lower:
            return 'Premium PVC Material'
        elif 'rubber' in product_lower:
            return 'Industrial Rubber'
        elif 'steel' in product_lower or 'container' in product_lower:
            return 'Galvanized Steel'
        elif 'wood' in product_lower:
            return 'Engineered Wood'
        else:
            return 'High-Quality Industrial Grade Materials'

    def generate_product_details(self, product: str, product_type: str) -> str:
        """Generate detailed product description"""
        details = f'''
<h2>Product Details</h2>

<p>Our {product.title()} represents the pinnacle of Chinese manufacturing excellence. Designed with precision engineering and built to meet international standards, this product delivers exceptional performance across various applications.</p>

<h3>Key Features</h3>
<ul>
<li><strong>Superior Quality:</strong> Manufactured using premium materials and advanced production techniques</li>
<li><strong>Competitive Pricing:</strong> Direct factory pricing offers significant cost savings</li>
<li><strong>Global Export Ready:</strong> Compliant with international export standards and certifications</li>
<li><strong>Customization Available:</strong> Tailored solutions to meet specific requirements</li>
<li><strong>Reliable Supply:</strong> Stable production capacity ensuring timely delivery</li>
</ul>

<h3>Applications</h3>
<p>Our {product.title()} is widely used in:</p>
<ul>
<li>Industrial facilities and manufacturing plants</li>
<li>Commercial buildings and warehouses</li>
<li>Residential and commercial flooring</li>
<li>Outdoor installations and heavy-duty applications</li>
<li>Export to global markets worldwide</li>
</ul>
'''
        return details

    def generate_selling_points(self, product: str) -> str:
        """Generate compelling selling points"""
        points = [
            'Factory direct pricing - No middleman markup',
            'ISO 9001 certified manufacturing process',
            'Fast global shipping to over 50 countries',
            'Professional technical support and consultation',
            'Custom design and OEM/ODM services available',
            'Sample orders welcome for quality verification',
            'Complete export documentation provided',
            'Responsive customer service team'
        ]

        html = '''<h2>Why Choose Our Product?</h2>
<div class="selling-points">
<ul>
'''
        for point in points:
            html += f'<li>{point}</li>\n'

        html += '</ul></div>'
        return html

    def generate_technical_highlights(self, product: str) -> str:
        """Generate technical highlights section"""
        highlights = [
            'Advanced manufacturing technology ensures precision and consistency',
            'Rigorous quality control processes at every production stage',
            'Environmentally friendly materials and production methods',
            'Long-lasting durability reducing replacement costs',
            'Easy installation and minimal maintenance requirements'
        ]

        html = '''<h2>Technical Highlights</h2>
<ol>
'''
        for highlight in highlights:
            html += f'<li>{highlight}</li>\n'

        html += '</ol>'
        return html

    def generate_international_trade_info(self, product: str) -> str:
        """Generate international trade information"""
        html = f'''
<h2>Export Information</h2>

<p>We specialize in international trade and export services, serving clients globally. Our experienced logistics team ensures safe and timely delivery to your specified location.</p>

<h3>Export Advantages</h3>
<ul>
<li>Competitive freight rates through established shipping partners</li>
<li>Complete export documentation (Bill of Lading, Commercial Invoice, Certificate of Origin)</li>
<li>Customs clearance assistance available</li>
<li>Insurance coverage for shipment protection</li>
<li>Flexible payment terms for international buyers</li>
</ul>

<h3>Global Market Reach</h3>
<p>Our products are exported to major markets including North America, Europe, Southeast Asia, Middle East, Australia, and South America. We understand the requirements of different markets and ensure compliance with local regulations.</p>
'''
        return html

    def generate_cta(self) -> str:
        """Generate Call-to-Action section"""
        return f'''
<div class="contact-cta">
<h2>Contact Us Today</h2>
<p>Ready to place an order or need more information? Contact our team for a free quote and consultation.</p>

<p><strong>Email:</strong> {self.target_email}</p>
<p>We respond within 24 hours with detailed product information and competitive pricing.</p>
</div>
'''

    def generate_full_content(self, topic: Dict, existing_posts: List[str] = None) -> Dict:
        """Generate complete SEO-optimized article content"""

        product = topic['product']
        keyword = topic['keyword']
        title = topic['title']

        # Generate all content sections
        content_parts = []

        # Introduction
        intro = f'''
<h1>{title}</h1>

<p><strong>Looking for high-quality {keyword} from China?</strong> As a leading manufacturer and exporter, we provide premium products at factory-direct prices for global markets. Our commitment to quality and customer satisfaction has made us a trusted partner for businesses worldwide.</p>

<p>In today's global marketplace, finding reliable suppliers is crucial. Our {keyword} combines superior quality with competitive pricing, making us the ideal choice for international buyers seeking dependable products.</p>
'''
        content_parts.append(intro)

        # Product specifications table
        content_parts.append(self.generate_product_specs_table(product, topic.get('type', 'existing')))

        # Product details
        content_parts.append(self.generate_product_details(product, topic.get('type', 'existing')))

        # Selling points
        content_parts.append(self.generate_selling_points(product))

        # Technical highlights
        content_parts.append(self.generate_technical_highlights(product))

        # International trade info
        content_parts.append(self.generate_international_trade_info(product))

        # CTA
        content_parts.append(self.generate_cta())

        # Combine all content
        full_content = '\n'.join(content_parts)

        # Generate meta description
        meta_description = f'Professional {keyword} manufacturer from China. Factory direct pricing, ISO certified, global export. Contact us for quotes and specifications.'

        # Generate excerpt
        excerpt = f'High-quality {keyword} from China. Professional manufacturer offering competitive prices, ISO certification, and global shipping. Contact {self.target_email} for details.'

        # Prepare result
        result = {
            'title': title,
            'content': full_content,
            'excerpt': excerpt,
            'meta_description': meta_description,
            'keyword': keyword,
            'slug': topic.get('slug', keyword.replace(' ', '-')),
            'external_links': self._get_relevant_external_links(keyword),
            'internal_links': self._get_internal_links(existing_posts or [], keyword)
        }

        return result

    def _get_relevant_external_links(self, keyword: str) -> List[Dict]:
        """Get relevant external links for SEO"""
        links = []

        # Select random external links
        selected = random.sample(self.external_links, min(2, len(self.external_links)))

        for link in selected:
            # Add keyword-relevant page
            if 'iso' in link:
                links.append({
                    'url': f'{link}standards/',
                    'text': f'International {keyword.title()} Standards'
                })
            elif 'wikipedia' in link:
                links.append({
                    'url': f'{link}{keyword.replace(" ", "_")}',
                    'text': f'Learn more about {keyword.title()}'
                })
            elif 'osha' in link:
                links.append({
                    'url': link,
                    'text': 'Safety Standards and Regulations'
                })

        return links

    def _get_internal_links(self, existing_posts: List[str], keyword: str) -> List[Dict]:
        """Get internal links to existing posts"""
        links = []

        if existing_posts:
            # Get 2 random existing posts
            selected = random.sample(existing_posts[:10], min(2, len(existing_posts)))

            for post_url in selected:
                links.append({
                    'url': post_url,
                    'text': 'View related products'
                })

        return links


def generate_content(topic: Dict, config: Dict) -> Dict:
    """Helper function to generate content"""
    generator = ContentGenerator(
        target_email=config['target_email'],
        external_links=config['external_links']
    )
    return generator.generate_full_content(topic, config.get('existing_posts', []))
