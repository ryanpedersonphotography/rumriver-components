#!/usr/bin/env python3
"""
Advanced Component Extractor with Descriptive Names and Filtering System
"""

import os
import re
from bs4 import BeautifulSoup
import hashlib
from collections import Counter

class AdvancedComponentExtractor:
    def __init__(self, directory):
        self.directory = directory
        self.components = []
        self.component_id = 1
        
    def scan_directory(self):
        """Scan directory for HTML files"""
        html_files = []
        for file in os.listdir(self.directory):
            if file.endswith('.html') and 'component' not in file.lower() and 'library' not in file.lower():
                html_files.append(os.path.join(self.directory, file))
        return sorted(html_files)
    
    def analyze_component_features(self, element):
        """Analyze component to extract its features for better naming"""
        features = []
        
        # Check for specific UI patterns
        element_str = str(element).lower()
        
        # Layout features
        if 'grid' in element_str or 'grid-template' in element_str:
            features.append('Grid Layout')
        if 'flex' in element_str or 'display: flex' in element_str:
            features.append('Flexbox')
        if 'fixed' in element_str and 'position' in element_str:
            features.append('Fixed Position')
        if 'sticky' in element_str:
            features.append('Sticky')
            
        # Visual features
        if 'gradient' in element_str:
            features.append('Gradient')
        if 'backdrop-filter' in element_str or 'blur' in element_str:
            features.append('Glass Effect')
        if 'shadow' in element_str:
            features.append('Shadow')
        if 'border-radius' in element_str:
            features.append('Rounded')
        if 'transform' in element_str or 'animation' in element_str:
            features.append('Animated')
        if 'hover' in element_str:
            features.append('Hover Effects')
            
        # Content features
        imgs = element.find_all('img')
        if imgs:
            features.append(f'{len(imgs)} Images')
        
        buttons = element.find_all(['button', 'a'])
        if buttons:
            btn_count = len([b for b in buttons if 'btn' in str(b).lower() or 'button' in str(b).lower()])
            if btn_count > 0:
                features.append(f'{btn_count} Buttons')
        
        forms = element.find_all('form')
        if forms:
            features.append('Form')
            
        inputs = element.find_all(['input', 'textarea', 'select'])
        if inputs:
            features.append(f'{len(inputs)} Inputs')
            
        # Interactive features
        if 'carousel' in element_str or 'slider' in element_str:
            features.append('Slider')
        if 'tab' in element_str:
            features.append('Tabs')
        if 'accordion' in element_str:
            features.append('Accordion')
        if 'modal' in element_str or 'popup' in element_str:
            features.append('Modal')
        if 'dropdown' in element_str:
            features.append('Dropdown')
            
        # Responsive features
        if '@media' in element_str or 'responsive' in element_str:
            features.append('Responsive')
        if 'mobile' in element_str:
            features.append('Mobile Optimized')
            
        return features
    
    def generate_descriptive_name(self, element, category, file_name):
        """Generate a descriptive name based on component analysis"""
        
        # Get basic identifiers
        classes = element.get('class', [])
        elem_id = element.get('id', '')
        tag_name = element.name
        
        # Analyze features
        features = self.analyze_component_features(element)
        
        # Build descriptive name
        name_parts = []
        
        # Add main identifier
        if elem_id:
            name_parts.append(elem_id.replace('-', ' ').replace('_', ' ').title())
        elif classes:
            main_class = classes[0] if isinstance(classes, list) else classes
            name_parts.append(main_class.replace('-', ' ').replace('_', ' ').title())
        else:
            name_parts.append(tag_name.title())
        
        # Add category if not redundant
        if category.lower() not in ' '.join(name_parts).lower():
            name_parts.append(f"({category.title()})")
        
        # Add key features
        if features:
            feature_str = ' - ' + ', '.join(features[:3])  # Limit to 3 features
            name_parts.append(feature_str)
        
        # Add file context if meaningful
        file_context = os.path.basename(file_name).replace('.html', '').replace('-', ' ')
        if 'venue' in file_context.lower() and 'venue' not in ' '.join(name_parts).lower():
            name_parts.append(f"[{file_context.title()[:20]}]")
        
        final_name = ' '.join(name_parts)
        return final_name[:80]  # Limit total length
    
    def extract_component_tags(self, element):
        """Extract tags for filtering"""
        tags = set()
        element_str = str(element).lower()
        
        # Style tags
        if 'gradient' in element_str:
            tags.add('gradient')
        if 'grid' in element_str:
            tags.add('grid')
        if 'flex' in element_str:
            tags.add('flexbox')
        if 'animated' in element_str or 'animation' in element_str:
            tags.add('animated')
        if 'responsive' in element_str or '@media' in element_str:
            tags.add('responsive')
        if 'hover' in element_str:
            tags.add('interactive')
            
        # Component type tags
        if element.find_all('form'):
            tags.add('form')
        if element.find_all('img'):
            tags.add('images')
        if element.find_all(['button', 'a']):
            tags.add('buttons')
        if 'carousel' in element_str or 'slider' in element_str:
            tags.add('slider')
        if 'modal' in element_str:
            tags.add('modal')
        if 'card' in element_str:
            tags.add('cards')
            
        # Color scheme tags
        if 'dark' in element_str or '#2c2416' in element_str:
            tags.add('dark-theme')
        if 'light' in element_str or '#faf6f2' in element_str:
            tags.add('light-theme')
            
        # Size tags
        element_size = len(str(element))
        if element_size < 500:
            tags.add('small')
        elif element_size < 2000:
            tags.add('medium')
        else:
            tags.add('large')
            
        return list(tags)
    
    def extract_major_components(self, soup, file_name):
        """Extract major structural components with enhanced metadata"""
        components = []
        
        # Enhanced component selectors with better categorization
        major_selectors = [
            ('header', 'NAVIGATION'),
            ('nav', 'NAVIGATION'),
            ('.navigation', 'NAVIGATION'),
            ('.navbar', 'NAVIGATION'),
            
            ('.hero', 'HERO SECTIONS'),
            ('.banner', 'HERO SECTIONS'),
            ('.showcase', 'HERO SECTIONS'),
            ('.jumbotron', 'HERO SECTIONS'),
            
            ('.gallery', 'GALLERIES'),
            ('.portfolio', 'GALLERIES'),
            ('.image-grid', 'GALLERIES'),
            ('.instagram', 'GALLERIES'),
            
            ('.services', 'SERVICE SECTIONS'),
            ('.features', 'SERVICE SECTIONS'),
            ('.benefits', 'SERVICE SECTIONS'),
            
            ('.testimonial', 'TESTIMONIALS'),
            ('.reviews', 'TESTIMONIALS'),
            ('.feedback', 'TESTIMONIALS'),
            
            ('.pricing', 'PRICING'),
            ('.packages', 'PRICING'),
            ('.plans', 'PRICING'),
            
            ('.contact', 'CONTACT FORMS'),
            ('form', 'CONTACT FORMS'),
            ('.booking', 'CONTACT FORMS'),
            
            ('footer', 'FOOTERS'),
            ('.footer', 'FOOTERS'),
            
            ('.card', 'CARDS & BLOCKS'),
            ('.block', 'CARDS & BLOCKS'),
            ('.item', 'CARDS & BLOCKS'),
            
            ('.accordion', 'INTERACTIVE'),
            ('.tabs', 'INTERACTIVE'),
            ('.modal', 'INTERACTIVE'),
            ('.popup', 'INTERACTIVE'),
            ('.slider', 'INTERACTIVE'),
            ('.carousel', 'INTERACTIVE'),
            
            ('section', 'CONTENT SECTIONS'),
            ('.section', 'CONTENT SECTIONS'),
        ]
        
        seen_hashes = set()
        
        for selector, category in major_selectors:
            if selector.startswith('.'):
                elements = soup.select(selector)
            else:
                elements = soup.find_all(selector)
            
            for elem in elements[:5]:  # Increased limit
                if elem and len(str(elem)) > 100:
                    elem_hash = hashlib.md5(str(elem).encode()).hexdigest()[:8]
                    if elem_hash not in seen_hashes:
                        seen_hashes.add(elem_hash)
                        
                        # Generate descriptive name
                        name = self.generate_descriptive_name(elem, category, file_name)
                        
                        # Extract tags for filtering
                        tags = self.extract_component_tags(elem)
                        
                        # Get a brief description
                        text_content = elem.get_text(strip=True)[:100]
                        
                        components.append({
                            'id': f'comp-{self.component_id}',
                            'name': name,
                            'category': category,
                            'file_source': os.path.basename(file_name),
                            'html': str(elem)[:3000],  # Increased size
                            'hash': elem_hash,
                            'tags': tags,
                            'description': text_content[:100] if text_content else 'No text content',
                            'size': len(str(elem))
                        })
                        self.component_id += 1
        
        return components
    
    def process_file(self, file_path):
        """Process a single HTML file"""
        print(f"Processing: {os.path.basename(file_path)}")
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            return self.extract_major_components(soup, file_path)
            
        except Exception as e:
            print(f"  ⚠ Error: {e}")
            return []
    
    def generate_html_library(self):
        """Generate enhanced HTML library with filtering"""
        
        # Group components by category
        categories = {}
        all_tags = set()
        
        for comp in self.components:
            cat = comp['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(comp)
            all_tags.update(comp.get('tags', []))
        
        # Generate filter buttons
        filter_buttons = []
        for tag in sorted(all_tags):
            filter_buttons.append(f'<button class="filter-btn" onclick="filterByTag(\'{tag}\')">{tag}</button>')
        
        # Generate accordion navigation with enhanced info
        nav_items = []
        for category, comps in sorted(categories.items()):
            category_id = category.lower().replace(' ', '-').replace('&', 'and')
            nav_items.append(f'''
    <div class="accordion-item">
        <div class="accordion-header" onclick="toggleAccordion('{category_id}')">
            <span>{category} <span class="category-count">{len(comps)}</span></span>
            <span class="accordion-arrow">▼</span>
        </div>
        <div class="accordion-content" id="accordion-{category_id}">''')
            
            for comp in comps:
                comp_name = comp["name"][:45] + "..." if len(comp["name"]) > 45 else comp["name"]
                tags_str = ' '.join(comp.get('tags', []))
                nav_items.append(f'''            <a href="#{comp["id"]}" class="nav-item" data-tags="{tags_str}" onclick="scrollToComponent('{comp["id"]}')" title="{comp['name']}">
                <span class="nav-item-name">{comp_name}</span>
                <span class="nav-item-size">{comp['size']} bytes</span>
            </a>''')
            
            nav_items.append('        </div>\n    </div>')
        
        # Generate component cards with enhanced metadata
        component_cards = []
        for comp in self.components:
            html_escaped = comp['html'].replace('<', '&lt;').replace('>', '&gt;')
            tags_html = ' '.join([f'<span class="tag">{tag}</span>' for tag in comp.get('tags', [])])
            
            card_html = f'''
    <div class="component-card" id="{comp['id']}" data-tags="{' '.join(comp.get('tags', []))}">
        <div class="component-header">
            <div>
                <h2 class="component-title">{comp['name']}</h2>
                <p class="component-description">{comp.get('description', '')}</p>
            </div>
            <div class="component-meta">
                <span class="component-badge category">{comp['category']}</span>
                <span class="component-badge source">{comp['file_source']}</span>
                <span class="component-badge size">{comp['size']} bytes</span>
            </div>
        </div>
        <div class="component-tags">
            {tags_html}
        </div>
        <div class="component-body">
            <div class="code-section">
                <div class="code-header">
                    <span class="code-label">HTML CODE</span>
                    <div class="code-actions">
                        <button class="action-btn" onclick="previewComponent('{comp['id']}')">👁 Preview</button>
                        <button class="copy-btn" onclick="copyCode('{comp['id']}-code')">📋 Copy Code</button>
                    </div>
                </div>
                <pre class="code-block" id="{comp['id']}-code">{html_escaped}</pre>
            </div>
            <div class="preview-section" id="{comp['id']}-preview" style="display:none;">
                <div class="preview-header">
                    <span class="preview-label">LIVE PREVIEW</span>
                    <button class="close-preview" onclick="closePreview('{comp['id']}')">✕ Close</button>
                </div>
                <div class="preview-content">
                    {comp['html']}
                </div>
            </div>
        </div>
    </div>'''
            component_cards.append(card_html)
        
        # HTML Template with enhanced styling
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Component Library - {len(self.components)} Components</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f8f9fa;
        }}
        
        /* Navigation Sidebar */
        .nav-sidebar {{
            position: fixed;
            top: 0;
            left: 0;
            width: 350px;
            height: 100vh;
            background: #1a1a1a;
            overflow-y: auto;
            z-index: 1000;
            box-shadow: 2px 0 15px rgba(0,0,0,0.3);
        }}
        
        .nav-header {{
            background: linear-gradient(135deg, #8B6337 0%, #D4A574 100%);
            color: white;
            padding: 25px;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        
        .nav-header h2 {{
            font-size: 22px;
            margin-bottom: 12px;
            font-weight: 600;
        }}
        
        .component-stats {{
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }}
        
        .stat-badge {{
            background: rgba(255,255,255,0.2);
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
        }}
        
        /* Search and Filters */
        .search-container {{
            padding: 20px;
            background: #242424;
            border-bottom: 1px solid #3a3a3a;
        }}
        
        .search-input {{
            width: 100%;
            padding: 12px 20px;
            border: 2px solid #3a3a3a;
            border-radius: 25px;
            background: #1a1a1a;
            color: white;
            font-size: 14px;
            transition: all 0.3s ease;
        }}
        
        .search-input:focus {{
            outline: none;
            border-color: #8B6337;
            background: #2a2a2a;
        }}
        
        .filter-container {{
            padding: 15px 20px;
            background: #2a2a2a;
            border-bottom: 1px solid #3a3a3a;
        }}
        
        .filter-label {{
            color: #888;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
            display: block;
        }}
        
        .filter-buttons {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        
        .filter-btn {{
            padding: 5px 12px;
            background: #3a3a3a;
            color: #ddd;
            border: 1px solid #4a4a4a;
            border-radius: 15px;
            font-size: 11px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .filter-btn:hover {{
            background: #4a4a4a;
            color: white;
        }}
        
        .filter-btn.active {{
            background: #8B6337;
            color: white;
            border-color: #8B6337;
        }}
        
        /* Accordion Styles */
        .accordion-item {{
            border-bottom: 1px solid #3a3a3a;
        }}
        
        .accordion-header {{
            padding: 18px 25px;
            background: #2a2a2a;
            color: #D4A574;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s ease;
            user-select: none;
        }}
        
        .accordion-header:hover {{
            background: #3a3a3a;
            color: white;
        }}
        
        .accordion-header.active {{
            background: linear-gradient(90deg, #8B6337 0%, #D4A574 100%);
            color: white;
        }}
        
        .accordion-arrow {{
            transition: transform 0.3s ease;
            font-size: 14px;
        }}
        
        .accordion-header.active .accordion-arrow {{
            transform: rotate(180deg);
        }}
        
        .accordion-content {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
            background: #1a1a1a;
        }}
        
        .accordion-content.active {{
            max-height: 800px;
            overflow-y: auto;
        }}
        
        .category-count {{
            background: rgba(212, 165, 116, 0.2);
            color: #D4A574;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 11px;
            margin-left: 10px;
        }}
        
        .nav-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 25px 12px 35px;
            color: #ccc;
            text-decoration: none;
            font-size: 13px;
            transition: all 0.2s ease;
            border-left: 3px solid transparent;
        }}
        
        .nav-item:hover {{
            background: #2a2a2a;
            color: white;
            padding-left: 40px;
            border-left-color: #D4A574;
        }}
        
        .nav-item.active {{
            background: #3a3a3a;
            color: white;
            border-left-color: #8B6337;
        }}
        
        .nav-item-name {{
            flex: 1;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        
        .nav-item-size {{
            font-size: 10px;
            color: #666;
            margin-left: 10px;
        }}
        
        /* Main Content */
        .main-content {{
            margin-left: 350px;
            padding: 40px;
        }}
        
        .library-header {{
            background: linear-gradient(135deg, #8B6337 0%, #D4A574 100%);
            color: white;
            padding: 60px;
            margin: -40px -40px 40px;
            text-align: center;
            border-radius: 0 0 20px 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .library-header h1 {{
            font-size: 42px;
            margin-bottom: 15px;
            font-weight: 700;
        }}
        
        .library-header p {{
            font-size: 18px;
            opacity: 0.95;
        }}
        
        /* Component Cards */
        .component-card {{
            background: white;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            overflow: hidden;
            transition: all 0.3s ease;
        }}
        
        .component-card:hover {{
            box-shadow: 0 5px 25px rgba(0,0,0,0.15);
            transform: translateY(-2px);
        }}
        
        .component-header {{
            background: linear-gradient(135deg, #2a2a2a 0%, #3a3a3a 100%);
            color: white;
            padding: 25px 30px;
            display: flex;
            justify-content: space-between;
            align-items: start;
        }}
        
        .component-title {{
            font-size: 20px;
            margin: 0 0 8px 0;
            font-weight: 600;
        }}
        
        .component-description {{
            color: #aaa;
            font-size: 13px;
            margin: 0;
        }}
        
        .component-meta {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            align-items: flex-end;
        }}
        
        .component-badge {{
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .component-badge.category {{
            background: #8B6337;
            color: white;
        }}
        
        .component-badge.source {{
            background: #4a4a4a;
            color: #ddd;
        }}
        
        .component-badge.size {{
            background: #2a2a2a;
            color: #888;
        }}
        
        .component-tags {{
            padding: 15px 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}
        
        .tag {{
            padding: 4px 10px;
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 12px;
            font-size: 11px;
            color: #495057;
        }}
        
        .component-body {{
            padding: 0;
        }}
        
        .code-section {{
            border-bottom: 1px solid #e9ecef;
        }}
        
        .code-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #1a1a1a;
            padding: 15px 25px;
        }}
        
        .code-label {{
            color: #D4A574;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 600;
        }}
        
        .code-actions {{
            display: flex;
            gap: 10px;
        }}
        
        .action-btn, .copy-btn {{
            background: #8B6337;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.3s ease;
            font-weight: 600;
        }}
        
        .action-btn:hover, .copy-btn:hover {{
            background: #D4A574;
            transform: translateY(-1px);
        }}
        
        .code-block {{
            background: #1a1a1a;
            color: #e9ecef;
            padding: 25px;
            overflow-x: auto;
            max-height: 400px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 13px;
            line-height: 1.6;
        }}
        
        .preview-section {{
            background: white;
            border-top: 1px solid #e9ecef;
        }}
        
        .preview-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 25px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .preview-label {{
            color: #495057;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 600;
        }}
        
        .close-preview {{
            background: #dc3545;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
        }}
        
        .preview-content {{
            padding: 30px;
            max-height: 500px;
            overflow: auto;
        }}
        
        /* Clear Filters Button */
        .clear-filters {{
            padding: 8px 16px;
            background: #dc3545;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            margin-top: 10px;
            width: 100%;
        }}
        
        .clear-filters:hover {{
            background: #c82333;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .nav-sidebar {{
                transform: translateX(-100%);
                transition: transform 0.3s;
            }}
            .nav-sidebar.open {{
                transform: translateX(0);
            }}
            .main-content {{
                margin-left: 0;
            }}
            .menu-toggle {{
                display: block !important;
            }}
        }}
        
        .menu-toggle {{
            display: none;
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 1001;
            background: #1a1a1a;
            color: white;
            border: none;
            padding: 12px 18px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }}
        
        /* Hidden class for filtering */
        .hidden {{
            display: none !important;
        }}
    </style>
</head>
<body>

<button class="menu-toggle" onclick="toggleMenu()">☰ Components</button>

<nav class="nav-sidebar" id="navSidebar">
    <div class="nav-header">
        <h2>📚 Advanced Component Library</h2>
        <div class="component-stats">
            <span class="stat-badge">{len(self.components)} Components</span>
            <span class="stat-badge">{len(categories)} Categories</span>
        </div>
    </div>
    
    <div class="search-container">
        <input type="text" 
               class="search-input" 
               placeholder="Search components by name or content..." 
               oninput="searchComponents(this.value)">
    </div>
    
    <div class="filter-container">
        <span class="filter-label">Quick Filters</span>
        <div class="filter-buttons">
            {' '.join(filter_buttons[:12])}
        </div>
        <button class="clear-filters" onclick="clearAllFilters()">Clear All Filters</button>
    </div>
    
    {''.join(nav_items)}
</nav>

<div class="main-content">
    <div class="library-header">
        <h1>Advanced Component Library</h1>
        <p>Comprehensive collection with descriptive names, tags, and filtering</p>
    </div>
    
    <div id="active-filters" style="margin-bottom: 20px; display: none;">
        <div style="padding: 15px; background: #fff; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.08);">
            <strong>Active Filters:</strong> <span id="filter-list"></span>
        </div>
    </div>
    
    {''.join(component_cards)}
</div>

<script>
let activeFilters = new Set();

function toggleMenu() {{
    document.getElementById('navSidebar').classList.toggle('open');
}}

function toggleAccordion(categoryId) {{
    const content = document.getElementById('accordion-' + categoryId);
    const header = event.currentTarget;
    
    content.classList.toggle('active');
    header.classList.toggle('active');
}}

function scrollToComponent(componentId) {{
    const element = document.getElementById(componentId);
    if (element) {{
        element.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
        
        // Highlight effect
        element.style.border = '3px solid #8B6337';
        element.style.boxShadow = '0 0 20px rgba(139, 99, 55, 0.3)';
        setTimeout(() => {{
            element.style.border = '';
            element.style.boxShadow = '';
        }}, 2000);
    }}
}}

function copyCode(elementId) {{
    const codeBlock = document.getElementById(elementId);
    const text = codeBlock.textContent;
    
    navigator.clipboard.writeText(text).then(() => {{
        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = '✅ Copied!';
        btn.style.background = '#28a745';
        
        setTimeout(() => {{
            btn.textContent = originalText;
            btn.style.background = '#8B6337';
        }}, 2000);
    }}).catch(err => {{
        alert('Failed to copy code. Please select and copy manually.');
    }});
}}

function previewComponent(componentId) {{
    const previewSection = document.getElementById(componentId + '-preview');
    if (previewSection) {{
        previewSection.style.display = previewSection.style.display === 'none' ? 'block' : 'none';
    }}
}}

function closePreview(componentId) {{
    const previewSection = document.getElementById(componentId + '-preview');
    if (previewSection) {{
        previewSection.style.display = 'none';
    }}
}}

function searchComponents(query) {{
    const components = document.querySelectorAll('.component-card');
    const navItems = document.querySelectorAll('.nav-item');
    
    query = query.toLowerCase();
    
    if (!query) {{
        components.forEach(comp => comp.classList.remove('hidden'));
        navItems.forEach(item => item.style.display = 'flex');
        return;
    }}
    
    // Filter components
    components.forEach(comp => {{
        const text = comp.textContent.toLowerCase();
        const tags = comp.dataset.tags || '';
        const shouldShow = text.includes(query) || tags.includes(query);
        
        if (shouldShow) {{
            comp.classList.remove('hidden');
        }} else {{
            comp.classList.add('hidden');
        }}
    }});
    
    // Filter navigation items
    navItems.forEach(item => {{
        const text = item.textContent.toLowerCase();
        const tags = item.dataset.tags || '';
        const shouldShow = text.includes(query) || tags.includes(query);
        item.style.display = shouldShow ? 'flex' : 'none';
    }});
    
    // Auto-expand accordions with matches
    document.querySelectorAll('.accordion-content').forEach(acc => {{
        const hasVisibleItems = Array.from(acc.querySelectorAll('.nav-item'))
            .some(item => item.style.display !== 'none');
        
        if (hasVisibleItems) {{
            acc.classList.add('active');
            acc.previousElementSibling.classList.add('active');
        }}
    }});
}}

function filterByTag(tag) {{
    const btn = event.target;
    
    if (activeFilters.has(tag)) {{
        activeFilters.delete(tag);
        btn.classList.remove('active');
    }} else {{
        activeFilters.add(tag);
        btn.classList.add('active');
    }}
    
    applyFilters();
}}

function applyFilters() {{
    const components = document.querySelectorAll('.component-card');
    const navItems = document.querySelectorAll('.nav-item');
    
    if (activeFilters.size === 0) {{
        components.forEach(comp => comp.classList.remove('hidden'));
        navItems.forEach(item => item.style.display = 'flex');
        document.getElementById('active-filters').style.display = 'none';
        return;
    }}
    
    // Show active filters
    document.getElementById('active-filters').style.display = 'block';
    document.getElementById('filter-list').textContent = Array.from(activeFilters).join(', ');
    
    // Apply filters
    components.forEach(comp => {{
        const tags = comp.dataset.tags || '';
        const hasAllTags = Array.from(activeFilters).every(filter => tags.includes(filter));
        
        if (hasAllTags) {{
            comp.classList.remove('hidden');
        }} else {{
            comp.classList.add('hidden');
        }}
    }});
    
    navItems.forEach(item => {{
        const tags = item.dataset.tags || '';
        const hasAllTags = Array.from(activeFilters).every(filter => tags.includes(filter));
        item.style.display = hasAllTags ? 'flex' : 'none';
    }});
}}

function clearAllFilters() {{
    activeFilters.clear();
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    applyFilters();
}}

// Initialize - open first accordion
document.addEventListener('DOMContentLoaded', () => {{
    const firstAccordion = document.querySelector('.accordion-content');
    const firstHeader = document.querySelector('.accordion-header');
    if (firstAccordion && firstHeader) {{
        firstAccordion.classList.add('active');
        firstHeader.classList.add('active');
    }}
}});
</script>

</body>
</html>'''
        
        return html
    
    def run(self):
        """Run the extraction"""
        print("=" * 60)
        print("ADVANCED COMPONENT EXTRACTION")
        print("=" * 60)
        
        html_files = self.scan_directory()
        print(f"Processing {len(html_files)} HTML files...\n")
        
        for file_path in html_files:
            components = self.process_file(file_path)
            self.components.extend(components)
            print(f"  ✓ Extracted {len(components)} components with enhanced metadata")
        
        print(f"\n{'=' * 60}")
        print(f"Total components extracted: {len(self.components)}")
        
        # Show sample of generated names
        print("\nSample of generated component names:")
        for comp in self.components[:5]:
            print(f"  • {comp['name']}")
        
        print("\nGenerating enhanced HTML library...")
        
        html_output = self.generate_html_library()
        
        output_path = os.path.join(self.directory, 'component-library-advanced.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        print(f"\n✅ Success! Advanced library saved to:")
        print(f"   {output_path}")
        
        return output_path

if __name__ == "__main__":
    directory = "/Users/ryanpederson/Downloads/rumrivercomponents/New Folder With Items"
    extractor = AdvancedComponentExtractor(directory)
    extractor.run()