#!/usr/bin/env python3
"""
Component Extractor for Barn Venue HTML Files
Automatically extracts all components from HTML files and creates a comprehensive library
"""

import os
import re
from bs4 import BeautifulSoup
import hashlib
from pathlib import Path

class ComponentExtractor:
    def __init__(self, directory):
        self.directory = directory
        self.components = []
        self.component_id = 1
        
        # Define component patterns to search for
        self.component_patterns = {
            'headers': ['header', 'nav', 'navigation', 'navbar', 'menu'],
            'heroes': ['hero', 'banner', 'jumbotron', 'showcase'],
            'galleries': ['gallery', 'portfolio', 'grid', 'masonry', 'instagram'],
            'forms': ['form', 'contact', 'booking', 'reservation'],
            'cards': ['card', 'service', 'pricing', 'package', 'testimonial', 'review'],
            'sections': ['section', 'feature', 'about', 'content', 'block'],
            'footers': ['footer'],
            'modals': ['modal', 'popup', 'overlay'],
            'sliders': ['slider', 'carousel', 'slideshow'],
            'tabs': ['tab', 'accordion', 'toggle'],
            'dividers': ['divider', 'separator', 'shape'],
            'animations': ['animation', 'parallax', 'scroll'],
            'buttons': ['btn', 'button', 'cta'],
            'teams': ['team', 'staff', 'member'],
            'maps': ['map', 'location', 'direction'],
            'social': ['social', 'share', 'proof'],
            'stats': ['stat', 'counter', 'number'],
            'blogs': ['blog', 'article', 'post', 'news'],
            'faqs': ['faq', 'question', 'accordion']
        }
    
    def scan_directory(self):
        """Scan directory for HTML files"""
        html_files = []
        for file in os.listdir(self.directory):
            if file.endswith('.html') and file != 'barn-venue-components-complete.html':
                html_files.append(os.path.join(self.directory, file))
        return sorted(html_files)
    
    def extract_component_from_element(self, element, file_name, component_type):
        """Extract a component from an HTML element"""
        # Get the element's classes and id
        classes = element.get('class', [])
        elem_id = element.get('id', '')
        
        # Generate component name
        class_str = ' '.join(classes) if classes else ''
        identifier = elem_id or class_str or element.name
        
        # Extract relevant CSS
        css = self.extract_css_for_component(element, file_name)
        
        # Extract JavaScript if present
        js = self.extract_js_for_component(element, file_name)
        
        # Create component object
        component = {
            'id': f'comp-{self.component_id}',
            'name': self.generate_component_name(identifier, component_type),
            'category': component_type.upper(),
            'file_source': os.path.basename(file_name),
            'html': str(element.prettify()),
            'css': css,
            'js': js,
            'description': self.generate_description(element, component_type),
            'hash': hashlib.md5(str(element).encode()).hexdigest()[:8]
        }
        
        self.component_id += 1
        return component
    
    def extract_css_for_component(self, element, file_content):
        """Extract CSS rules related to the component"""
        css_rules = []
        
        # Get all classes and IDs from the element and its children
        selectors = set()
        
        # Add element's own classes and ID
        if element.get('class'):
            for cls in element.get('class'):
                selectors.add(f'.{cls}')
        if element.get('id'):
            selectors.add(f'#{element.get("id")}')
        
        # Add children's classes and IDs
        for child in element.find_all():
            if child.get('class'):
                for cls in child.get('class'):
                    selectors.add(f'.{cls}')
            if child.get('id'):
                selectors.add(f'#{child.get("id")}')
        
        # Extract CSS from style tags
        if isinstance(file_content, str):
            soup = BeautifulSoup(file_content, 'html.parser')
        else:
            soup = file_content
            
        for style_tag in soup.find_all('style'):
            style_content = style_tag.string
            if style_content:
                # Simple CSS extraction - looks for rules containing our selectors
                for selector in selectors:
                    # Find CSS rules containing this selector
                    pattern = rf'{re.escape(selector)}[^{{]*{{[^}}]*}}'
                    matches = re.findall(pattern, style_content, re.MULTILINE | re.DOTALL)
                    css_rules.extend(matches)
        
        return '\n'.join(set(css_rules))  # Remove duplicates
    
    def extract_js_for_component(self, element, file_content):
        """Extract JavaScript related to the component"""
        js_code = []
        
        # Get element ID for JS references
        elem_id = element.get('id', '')
        
        if elem_id:
            # Look for JavaScript that references this ID
            if isinstance(file_content, str):
                soup = BeautifulSoup(file_content, 'html.parser')
            else:
                soup = file_content
                
            for script_tag in soup.find_all('script'):
                script_content = script_tag.string
                if script_content and elem_id in script_content:
                    js_code.append(script_content)
        
        return '\n'.join(js_code)
    
    def generate_component_name(self, identifier, component_type):
        """Generate a readable component name"""
        # Clean up the identifier
        name = identifier.replace('-', ' ').replace('_', ' ')
        name = ' '.join(word.capitalize() for word in name.split())
        
        # Add component type if not already in name
        if component_type.lower() not in name.lower():
            name = f"{component_type.capitalize()} - {name}"
        
        return name[:50]  # Limit length
    
    def generate_description(self, element, component_type):
        """Generate a description for the component"""
        # Count child elements
        child_count = len(element.find_all())
        
        # Check for specific features
        features = []
        if element.find_all('img'):
            features.append('images')
        if element.find_all('button') or element.find_all(class_=re.compile('btn')):
            features.append('buttons')
        if element.find_all('form'):
            features.append('form elements')
        if element.find_all('a'):
            features.append('links')
        
        description = f"A {component_type} component"
        if features:
            description += f" containing {', '.join(features)}"
        description += f". Contains {child_count} child elements."
        
        return description
    
    def process_file(self, file_path):
        """Process a single HTML file to extract components"""
        print(f"Processing: {os.path.basename(file_path)}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            file_components = []
            
            # Search for components by patterns
            for category, patterns in self.component_patterns.items():
                for pattern in patterns:
                    # Search by class name
                    elements = soup.find_all(class_=re.compile(pattern, re.I))
                    for elem in elements:
                        if self.is_significant_element(elem):
                            component = self.extract_component_from_element(elem, content, category)
                            if not self.is_duplicate(component):
                                file_components.append(component)
                    
                    # Search by ID
                    elements = soup.find_all(id=re.compile(pattern, re.I))
                    for elem in elements:
                        if self.is_significant_element(elem):
                            component = self.extract_component_from_element(elem, content, category)
                            if not self.is_duplicate(component):
                                file_components.append(component)
                    
                    # Search by tag name for specific patterns
                    if pattern in ['header', 'footer', 'nav', 'section', 'form']:
                        elements = soup.find_all(pattern)
                        for elem in elements:
                            if self.is_significant_element(elem):
                                component = self.extract_component_from_element(elem, content, category)
                                if not self.is_duplicate(component):
                                    file_components.append(component)
            
            return file_components
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return []
    
    def is_significant_element(self, element):
        """Check if an element is significant enough to be a component"""
        # Must have some content
        if not element.get_text(strip=True):
            return False
        
        # Must have reasonable size (not just a wrapper)
        child_count = len(element.find_all())
        if child_count < 2:
            return False
        
        # Should not be too small
        text_length = len(element.get_text(strip=True))
        if text_length < 20:
            return False
        
        return True
    
    def is_duplicate(self, component):
        """Check if component is a duplicate based on hash"""
        for existing in self.components:
            if existing['hash'] == component['hash']:
                return True
        return False
    
    def generate_html_library(self):
        """Generate the final HTML component library"""
        html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Auto-Generated Component Library - {component_count} Components</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Georgia', serif; background: #FAF6F2; }}
        
        /* Navigation */
        .nav-sidebar {{
            position: fixed;
            top: 0;
            left: 0;
            width: 280px;
            height: 100vh;
            background: #2C2416;
            overflow-y: auto;
            z-index: 1000;
            box-shadow: 2px 0 10px rgba(0,0,0,0.2);
        }}
        
        .nav-header {{
            background: #8B6337;
            color: white;
            padding: 20px;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        
        .nav-header h2 {{
            font-size: 18px;
            margin-bottom: 10px;
        }}
        
        .component-count {{
            background: #D4A574;
            color: #2C2416;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
            display: inline-block;
        }}
        
        /* Accordion Styles */
        .accordion-item {{
            border-bottom: 1px solid #4A3426;
        }}
        
        .accordion-header {{
            padding: 15px 20px;
            background: #3A2F2A;
            color: #D4A574;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: bold;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s ease;
            user-select: none;
        }}
        
        .accordion-header:hover {{
            background: #4A3426;
            color: #FAF6F2;
        }}
        
        .accordion-header.active {{
            background: #8B6337;
            color: white;
        }}
        
        .accordion-arrow {{
            transition: transform 0.3s ease;
            font-size: 16px;
        }}
        
        .accordion-header.active .accordion-arrow {{
            transform: rotate(180deg);
        }}
        
        .accordion-content {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
            background: #1F1A14;
        }}
        
        .accordion-content.active {{
            max-height: 500px;
            overflow-y: auto;
        }}
        
        .category-count {{
            background: rgba(212, 165, 116, 0.3);
            color: #D4A574;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 10px;
            margin-left: 10px;
        }}
        
        .nav-item {{
            display: block;
            padding: 8px 20px 8px 30px;
            color: #FAF6F2;
            text-decoration: none;
            font-size: 13px;
            transition: all 0.3s ease;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            border-left: 3px solid transparent;
        }}
        
        .nav-item:hover {{
            background: #4A3426;
            color: #D4A574;
            padding-left: 35px;
            border-left-color: #D4A574;
        }}
        
        .nav-item.active {{
            background: #8B6337;
            color: white;
            border-left-color: #D4A574;
        }}
        
        /* Main Content */
        .main-content {{
            margin-left: 280px;
            padding: 40px;
        }}
        
        .library-header {{
            background: linear-gradient(135deg, #8B6337 0%, #4A3426 100%);
            color: white;
            padding: 60px 40px;
            margin: -40px -40px 40px;
            text-align: center;
        }}
        
        .library-header h1 {{
            font-size: 42px;
            margin-bottom: 20px;
        }}
        
        /* Component Cards */
        .component-card {{
            background: white;
            border-radius: 12px;
            margin-bottom: 40px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            overflow: hidden;
        }}
        
        .component-header {{
            background: linear-gradient(135deg, #8B6337 0%, #D4A574 100%);
            color: white;
            padding: 20px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .component-title {{
            font-size: 24px;
            margin: 0;
        }}
        
        .component-meta {{
            display: flex;
            gap: 10px;
            align-items: center;
        }}
        
        .component-badge {{
            background: rgba(255,255,255,0.2);
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
        }}
        
        .component-body {{
            padding: 30px;
        }}
        
        .component-description {{
            color: #6B5D54;
            margin-bottom: 20px;
            padding-bottom: 20px;
            border-bottom: 1px solid #E8D5C4;
        }}
        
        .component-preview {{
            background: #FAF6F2;
            border: 1px solid #E8D5C4;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            max-height: 400px;
            overflow: auto;
        }}
        
        .code-section {{
            margin-top: 20px;
        }}
        
        .code-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #1e1e1e;
            padding: 10px 20px;
            border-radius: 8px 8px 0 0;
        }}
        
        .code-label {{
            color: #D4A574;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .copy-btn {{
            background: #8B6337;
            color: white;
            border: none;
            padding: 5px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
        }}
        
        .copy-btn:hover {{
            background: #D4A574;
        }}
        
        .code-block {{
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            border-radius: 0 0 8px 8px;
            overflow-x: auto;
            max-height: 300px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.5;
        }}
        
        /* Search Bar */
        .search-container {{
            padding: 20px;
            background: #4A3426;
        }}
        
        .search-input {{
            width: 100%;
            padding: 10px 15px;
            border: none;
            border-radius: 25px;
            background: rgba(255,255,255,0.1);
            color: white;
            font-size: 14px;
        }}
        
        .search-input::placeholder {{
            color: rgba(255,255,255,0.5);
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .nav-sidebar {{ transform: translateX(-100%); transition: transform 0.3s; }}
            .nav-sidebar.open {{ transform: translateX(0); }}
            .main-content {{ margin-left: 0; padding: 20px; }}
            .menu-toggle {{
                position: fixed;
                top: 20px;
                left: 20px;
                z-index: 1001;
                background: #2C2416;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                cursor: pointer;
            }}
        }}
        
        .menu-toggle {{ display: none; }}
        @media (max-width: 768px) {{ .menu-toggle {{ display: block; }} }}
    </style>
</head>
<body>

<button class="menu-toggle" onclick="toggleMenu()">☰ Menu</button>

<!-- Navigation Sidebar -->
<nav class="nav-sidebar" id="navSidebar">
    <div class="nav-header">
        <h2>📚 Component Library</h2>
        <span class="component-count">{component_count} Components</span>
    </div>
    
    <div class="search-container">
        <input type="text" class="search-input" placeholder="Search components..." oninput="searchComponents(this.value)">
    </div>
    
    {navigation_items}
</nav>

<!-- Main Content -->
<div class="main-content">
    <div class="library-header">
        <h1>Auto-Extracted Component Library</h1>
        <p>Complete collection of {component_count} components from {file_count} HTML files</p>
    </div>
    
    {component_cards}
</div>

<script>
function toggleMenu() {{
    document.getElementById('navSidebar').classList.toggle('open');
}}

function toggleAccordion(categoryId) {{
    const content = document.getElementById('accordion-' + categoryId);
    const header = event.currentTarget;
    
    // Close all other accordions
    document.querySelectorAll('.accordion-content').forEach(acc => {{
        if (acc.id !== 'accordion-' + categoryId) {{
            acc.classList.remove('active');
        }}
    }});
    
    document.querySelectorAll('.accordion-header').forEach(h => {{
        if (h !== header) {{
            h.classList.remove('active');
        }}
    }});
    
    // Toggle current accordion
    content.classList.toggle('active');
    header.classList.toggle('active');
}}

function copyCode(elementId) {{
    const codeBlock = document.getElementById(elementId);
    const text = codeBlock.textContent;
    
    navigator.clipboard.writeText(text).then(() => {{
        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = '✓ Copied!';
        btn.style.background = '#4CAF50';
        
        setTimeout(() => {{
            btn.textContent = originalText;
            btn.style.background = '#8B6337';
        }}, 2000);
    }});
}}

function searchComponents(query) {{
    const components = document.querySelectorAll('.component-card');
    const navItems = document.querySelectorAll('.nav-item');
    const accordionHeaders = document.querySelectorAll('.accordion-header');
    
    query = query.toLowerCase();
    
    if (query === '') {{
        // Reset all if search is empty
        components.forEach(comp => comp.style.display = 'block');
        navItems.forEach(item => item.style.display = 'block');
        accordionHeaders.forEach(header => header.style.display = 'flex');
        return;
    }}
    
    // Track which categories have visible items
    const visibleCategories = new Set();
    
    components.forEach((comp) => {{
        const text = comp.textContent.toLowerCase();
        const shouldShow = text.includes(query);
        comp.style.display = shouldShow ? 'block' : 'none';
    }});
    
    navItems.forEach(item => {{
        const text = item.textContent.toLowerCase();
        const shouldShow = text.includes(query);
        item.style.display = shouldShow ? 'block' : 'none';
        
        if (shouldShow) {{
            // Find parent accordion and mark as visible
            const accordion = item.closest('.accordion-item');
            if (accordion) {{
                const header = accordion.querySelector('.accordion-header');
                const content = accordion.querySelector('.accordion-content');
                visibleCategories.add(accordion);
                // Auto-expand accordions with search results
                content.classList.add('active');
                header.classList.add('active');
            }}
        }}
    }});
    
    // Hide accordions with no visible items
    document.querySelectorAll('.accordion-item').forEach(accordion => {{
        accordion.style.display = visibleCategories.has(accordion) ? 'block' : 'none';
    }});
}}

// Highlight active component on scroll and auto-expand its accordion
document.addEventListener('DOMContentLoaded', () => {{
    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                const id = entry.target.id;
                
                // Remove all active states
                document.querySelectorAll('.nav-item').forEach(item => {{
                    item.classList.remove('active');
                }});
                
                // Set new active state
                const activeLink = document.querySelector(`[href="#${{id}}"]`);
                if (activeLink) {{
                    activeLink.classList.add('active');
                    
                    // Auto-expand parent accordion
                    const accordion = activeLink.closest('.accordion-item');
                    if (accordion) {{
                        const content = accordion.querySelector('.accordion-content');
                        const header = accordion.querySelector('.accordion-header');
                        if (!content.classList.contains('active')) {{
                            content.classList.add('active');
                            header.classList.add('active');
                        }}
                    }}
                }}
            }}
        }});
    }}, {{ threshold: 0.5 }});
    
    document.querySelectorAll('.component-card').forEach(card => {{
        observer.observe(card);
    }});
    
    // Open first accordion by default
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
        
        # Group components by category
        categories = {}
        for comp in self.components:
            cat = comp['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(comp)
        
        # Generate accordion navigation
        nav_items = []
        for category, comps in sorted(categories.items()):
            category_id = category.lower().replace(' ', '-')
            nav_items.append(f'''
    <div class="accordion-item">
        <div class="accordion-header" onclick="toggleAccordion('{category_id}')">
            <span>{category} <span class="category-count">{len(comps)}</span></span>
            <span class="accordion-arrow">▼</span>
        </div>
        <div class="accordion-content" id="accordion-{category_id}">''')
            
            # Add all components in this category
            for comp in comps:
                comp_name = comp["name"][:35] + "..." if len(comp["name"]) > 35 else comp["name"]
                nav_items.append(f'            <a href="#{comp["id"]}" class="nav-item">{comp_name}</a>')
            
            nav_items.append('        </div>')
            nav_items.append('    </div>')
        
        # Generate component cards
        component_cards = []
        for comp in self.components:
            # Escape HTML for display
            html_escaped = comp['html'].replace('<', '&lt;').replace('>', '&gt;')
            css_escaped = comp['css'].replace('<', '&lt;').replace('>', '&gt;') if comp['css'] else ''
            js_escaped = comp['js'].replace('<', '&lt;').replace('>', '&gt;') if comp['js'] else ''
            
            card_html = f'''
    <div class="component-card" id="{comp['id']}">
        <div class="component-header">
            <h2 class="component-title">{comp['name']}</h2>
            <div class="component-meta">
                <span class="component-badge">{comp['category']}</span>
                <span class="component-badge">{comp['file_source']}</span>
                <span class="component-badge">{comp['id']}</span>
            </div>
        </div>
        <div class="component-body">
            <p class="component-description">{comp['description']}</p>
            
            <div class="component-preview">
                {comp['html'][:500]}...
            </div>
            
            <div class="code-section">
                <div class="code-header">
                    <span class="code-label">HTML</span>
                    <button class="copy-btn" onclick="copyCode('{comp['id']}-html')">Copy HTML</button>
                </div>
                <pre class="code-block" id="{comp['id']}-html">{html_escaped}</pre>
            </div>
            '''
            
            if comp['css']:
                card_html += f'''
            <div class="code-section">
                <div class="code-header">
                    <span class="code-label">CSS</span>
                    <button class="copy-btn" onclick="copyCode('{comp['id']}-css')">Copy CSS</button>
                </div>
                <pre class="code-block" id="{comp['id']}-css">{css_escaped}</pre>
            </div>
            '''
            
            if comp['js']:
                card_html += f'''
            <div class="code-section">
                <div class="code-header">
                    <span class="code-label">JavaScript</span>
                    <button class="copy-btn" onclick="copyCode('{comp['id']}-js')">Copy JS</button>
                </div>
                <pre class="code-block" id="{comp['id']}-js">{js_escaped}</pre>
            </div>
            '''
            
            card_html += '''
        </div>
    </div>'''
            
            component_cards.append(card_html)
        
        # Fill template
        final_html = html_template.format(
            component_count=len(self.components),
            file_count=len(self.scan_directory()),
            navigation_items='\n    '.join(nav_items),
            component_cards='\n    '.join(component_cards)
        )
        
        return final_html
    
    def run(self):
        """Main execution method"""
        print("=" * 60)
        print("COMPONENT EXTRACTION STARTED")
        print("=" * 60)
        
        # Scan for HTML files
        html_files = self.scan_directory()
        print(f"\nFound {len(html_files)} HTML files to process")
        
        # Process each file
        for file_path in html_files:
            components = self.process_file(file_path)
            self.components.extend(components)
            print(f"  - Extracted {len(components)} components")
        
        # Remove duplicates one more time
        unique_components = []
        seen_hashes = set()
        for comp in self.components:
            if comp['hash'] not in seen_hashes:
                unique_components.append(comp)
                seen_hashes.add(comp['hash'])
        
        self.components = unique_components
        
        print(f"\n{'=' * 60}")
        print(f"EXTRACTION COMPLETE")
        print(f"Total unique components: {len(self.components)}")
        print(f"{'=' * 60}")
        
        # Generate HTML library
        print("\nGenerating HTML library...")
        html_output = self.generate_html_library()
        
        # Save to file
        output_path = os.path.join(self.directory, 'auto-component-library.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        print(f"\n✅ Component library saved to: {output_path}")
        print(f"✅ Total components extracted: {len(self.components)}")
        
        # Print summary by category
        print("\n📊 Components by Category:")
        category_counts = {}
        for comp in self.components:
            cat = comp['category']
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        for cat, count in sorted(category_counts.items()):
            print(f"  - {cat}: {count} components")
        
        return output_path

if __name__ == "__main__":
    # Set the directory containing HTML files
    directory = "/Users/ryanpederson/Downloads/rumrivercomponents/New Folder With Items"
    
    # Create extractor and run
    extractor = ComponentExtractor(directory)
    output_file = extractor.run()
    
    print(f"\n🎉 Success! Open {output_file} in your browser to view the component library.")