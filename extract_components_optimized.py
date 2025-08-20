#!/usr/bin/env python3
"""
Optimized Component Extractor with Accordion Navigation
"""

import os
import re
from bs4 import BeautifulSoup
import hashlib
from pathlib import Path

class OptimizedComponentExtractor:
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
        return sorted(html_files)[:10]  # Limit to first 10 files for testing
    
    def extract_major_components(self, soup, file_name):
        """Extract only major structural components"""
        components = []
        
        # Define major component selectors
        major_selectors = [
            ('header', 'HEADERS'),
            ('nav', 'NAVIGATION'),
            ('.hero', 'HEROES'),
            ('.gallery', 'GALLERIES'),
            ('.services', 'SERVICES'),
            ('.testimonial', 'TESTIMONIALS'),
            ('.pricing', 'PRICING'),
            ('.contact', 'FORMS'),
            ('footer', 'FOOTERS'),
            ('.section', 'SECTIONS'),
            ('.card', 'CARDS'),
            ('.accordion', 'ACCORDIONS'),
            ('.tabs', 'TABS'),
            ('.modal', 'MODALS'),
            ('.slider', 'SLIDERS')
        ]
        
        seen_hashes = set()
        
        for selector, category in major_selectors:
            if selector.startswith('.'):
                elements = soup.select(selector)
            else:
                elements = soup.find_all(selector)
            
            for elem in elements[:3]:  # Limit to 3 per type per file
                if elem and len(str(elem)) > 100:  # Must have substantial content
                    elem_hash = hashlib.md5(str(elem).encode()).hexdigest()[:8]
                    if elem_hash not in seen_hashes:
                        seen_hashes.add(elem_hash)
                        
                        # Generate component name
                        classes = elem.get('class', [])
                        elem_id = elem.get('id', '')
                        name = elem_id or (classes[0] if classes else elem.name)
                        
                        components.append({
                            'id': f'comp-{self.component_id}',
                            'name': name.replace('-', ' ').replace('_', ' ').title()[:40],
                            'category': category,
                            'file_source': os.path.basename(file_name),
                            'html': str(elem)[:2000],  # Limit HTML size
                            'hash': elem_hash
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
            print(f"Error processing {file_path}: {e}")
            return []
    
    def generate_html_library(self):
        """Generate the HTML library with accordion navigation"""
        
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
            
            for comp in comps:
                comp_name = comp["name"][:30] + "..." if len(comp["name"]) > 30 else comp["name"]
                nav_items.append(f'            <a href="#{comp["id"]}" class="nav-item" onclick="scrollToComponent(\'{comp["id"]}\')">{comp_name}</a>')
            
            nav_items.append('        </div>\n    </div>')
        
        # Generate component cards
        component_cards = []
        for comp in self.components:
            html_escaped = comp['html'].replace('<', '&lt;').replace('>', '&gt;')
            
            card_html = f'''
    <div class="component-card" id="{comp['id']}">
        <div class="component-header">
            <h2 class="component-title">{comp['name']}</h2>
            <div class="component-meta">
                <span class="component-badge">{comp['category']}</span>
                <span class="component-badge">{comp['file_source']}</span>
            </div>
        </div>
        <div class="component-body">
            <div class="code-section">
                <div class="code-header">
                    <span class="code-label">HTML CODE</span>
                    <button class="copy-btn" onclick="copyCode('{comp['id']}-code')">Copy Code</button>
                </div>
                <pre class="code-block" id="{comp['id']}-code">{html_escaped}</pre>
            </div>
        </div>
    </div>'''
            component_cards.append(card_html)
        
        # HTML Template
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Component Library - {len(self.components)} Components</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Georgia', serif; background: #FAF6F2; }}
        
        /* Navigation Sidebar */
        .nav-sidebar {{
            position: fixed;
            top: 0;
            left: 0;
            width: 300px;
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
            font-size: 20px;
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
            font-size: 12px;
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
            font-size: 14px;
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
            max-height: 600px;
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
            padding: 10px 20px 10px 35px;
            color: #FAF6F2;
            text-decoration: none;
            font-size: 13px;
            transition: all 0.3s ease;
            border-left: 3px solid transparent;
        }}
        
        .nav-item:hover {{
            background: #4A3426;
            color: #D4A574;
            padding-left: 40px;
            border-left-color: #D4A574;
        }}
        
        .nav-item.active {{
            background: #8B6337;
            color: white;
            border-left-color: #D4A574;
        }}
        
        /* Search Bar */
        .search-container {{
            padding: 15px;
            background: #4A3426;
            border-bottom: 1px solid #8B6337;
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
        
        /* Main Content */
        .main-content {{
            margin-left: 300px;
            padding: 40px;
        }}
        
        .library-header {{
            background: linear-gradient(135deg, #8B6337 0%, #4A3426 100%);
            color: white;
            padding: 60px 40px;
            margin: -40px -40px 40px;
            text-align: center;
            border-radius: 0 0 20px 20px;
        }}
        
        /* Component Cards */
        .component-card {{
            background: white;
            border-radius: 12px;
            margin-bottom: 30px;
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
            font-size: 22px;
            margin: 0;
        }}
        
        .component-meta {{
            display: flex;
            gap: 10px;
        }}
        
        .component-badge {{
            background: rgba(255,255,255,0.2);
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 11px;
        }}
        
        .component-body {{
            padding: 25px;
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
            padding: 6px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.3s ease;
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
            max-height: 400px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.6;
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
            background: #2C2416;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }}
    </style>
</head>
<body>

<button class="menu-toggle" onclick="toggleMenu()">☰ Components</button>

<nav class="nav-sidebar" id="navSidebar">
    <div class="nav-header">
        <h2>📚 Component Library</h2>
        <span class="component-count">{len(self.components)} Components</span>
    </div>
    
    <div class="search-container">
        <input type="text" class="search-input" placeholder="Search components..." oninput="searchComponents(this.value)">
    </div>
    
    {''.join(nav_items)}
</nav>

<div class="main-content">
    <div class="library-header">
        <h1>Component Library with Accordion Navigation</h1>
        <p>Extracted {len(self.components)} components from {len(categories)} categories</p>
    </div>
    
    {''.join(component_cards)}
</div>

<script>
function toggleMenu() {{
    document.getElementById('navSidebar').classList.toggle('open');
}}

function toggleAccordion(categoryId) {{
    const content = document.getElementById('accordion-' + categoryId);
    const header = event.currentTarget;
    
    // Toggle current accordion
    content.classList.toggle('active');
    header.classList.toggle('active');
}}

function scrollToComponent(componentId) {{
    const element = document.getElementById(componentId);
    if (element) {{
        element.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
        
        // Highlight the component briefly
        element.style.border = '3px solid #8B6337';
        setTimeout(() => {{
            element.style.border = '';
        }}, 2000);
    }}
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
    }}).catch(err => {{
        console.error('Failed to copy:', err);
    }});
}}

function searchComponents(query) {{
    const components = document.querySelectorAll('.component-card');
    const navItems = document.querySelectorAll('.nav-item');
    
    query = query.toLowerCase();
    
    // Show/hide components and nav items
    components.forEach(comp => {{
        const text = comp.textContent.toLowerCase();
        comp.style.display = text.includes(query) ? 'block' : 'none';
    }});
    
    navItems.forEach(item => {{
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(query) ? 'block' : 'none';
    }});
    
    // Auto-expand accordions with matches
    if (query) {{
        document.querySelectorAll('.accordion-content').forEach(acc => {{
            const hasVisibleItems = Array.from(acc.querySelectorAll('.nav-item'))
                .some(item => item.style.display !== 'none');
            
            if (hasVisibleItems) {{
                acc.classList.add('active');
                acc.previousElementSibling.classList.add('active');
            }}
        }});
    }}
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
        print("OPTIMIZED COMPONENT EXTRACTION")
        print("=" * 60)
        
        html_files = self.scan_directory()
        print(f"Processing {len(html_files)} HTML files...\n")
        
        for file_path in html_files:
            components = self.process_file(file_path)
            self.components.extend(components)
            print(f"  ✓ Found {len(components)} components")
        
        print(f"\n{'=' * 60}")
        print(f"Total components extracted: {len(self.components)}")
        print("Generating HTML library...")
        
        html_output = self.generate_html_library()
        
        output_path = os.path.join(self.directory, 'component-library-accordion.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        print(f"\n✅ Success! Library saved to:")
        print(f"   {output_path}")
        
        return output_path

if __name__ == "__main__":
    directory = "/Users/ryanpederson/Downloads/rumrivercomponents/New Folder With Items"
    extractor = OptimizedComponentExtractor(directory)
    extractor.run()