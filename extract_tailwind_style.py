#!/usr/bin/env python3
"""
Extract HTML components and create a Tailwind UI-style component library
Combines Astrum's simplicity with Tailwind's visual presentation
"""

import os
import re
import hashlib
from bs4 import BeautifulSoup, Comment
from collections import defaultdict
import json

class TailwindStyleExtractor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.components = []
        self.categories = defaultdict(list)
        self.seen_hashes = set()
        
    def extract_all_components(self):
        """Extract components from all HTML files"""
        html_files = [f for f in os.listdir(self.folder_path) 
                     if f.endswith('.html') and f != 'component-library-tailwind.html']
        
        for file_name in html_files:
            file_path = os.path.join(self.folder_path, file_name)
            self.extract_from_file(file_path, file_name)
        
        return self.categories
    
    def extract_from_file(self, file_path, file_name):
        """Extract meaningful components from a single HTML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
            
            # Remove scripts and styles for cleaner extraction
            for element in soup(['script', 'style']):
                element.decompose()
            
            # Extract sections and major components
            components = []
            
            # Look for common component patterns
            for selector in ['section', 'header', 'footer', '[class*="hero"]', 
                           '[class*="feature"]', '[class*="testimonial"]', 
                           '[class*="pricing"]', '[class*="cta"]', 'nav',
                           'div.container', 'div[class*="section"]']:
                elements = soup.select(selector)[:5]  # Limit per selector
                for element in elements:
                    if self.is_valid_component(element):
                        components.append(element)
            
            # Process and categorize components
            for component in components:
                self.process_component(component, file_name)
                
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
    
    def is_valid_component(self, element):
        """Check if element is a valid component"""
        if not element or not element.name:
            return False
        
        # Must have some content
        text_content = element.get_text(strip=True)
        if len(text_content) < 20:
            return False
        
        # Check for duplicate
        html_str = str(element)
        component_hash = hashlib.md5(html_str.encode()).hexdigest()
        if component_hash in self.seen_hashes:
            return False
        
        self.seen_hashes.add(component_hash)
        return True
    
    def get_component_category(self, element):
        """Determine component category based on content and structure"""
        classes = ' '.join(element.get('class', []))
        tag = element.name
        text = element.get_text(strip=True).lower()
        
        # Category detection logic
        if tag == 'nav' or 'nav' in classes:
            return "Navigation"
        elif tag == 'header' or 'header' in classes or 'hero' in classes:
            return "Heroes"
        elif tag == 'footer' or 'footer' in classes:
            return "Footers"
        elif 'testimonial' in classes or 'review' in text:
            return "Testimonials"
        elif 'pricing' in classes or 'price' in text:
            return "Pricing"
        elif 'feature' in classes or 'service' in classes:
            return "Features"
        elif 'cta' in classes or 'call-to-action' in text:
            return "CTA Sections"
        elif 'contact' in classes or 'contact' in text:
            return "Contact"
        elif 'gallery' in classes or element.find_all('img', limit=3):
            return "Content Sections"
        else:
            return "Page Sections"
    
    def get_component_name(self, element, category):
        """Generate a simple, descriptive name"""
        # Look for headings
        heading = element.find(['h1', 'h2', 'h3'])
        if heading:
            name = heading.get_text(strip=True)[:30]
            if name:
                return name
        
        # Count key elements
        features = []
        img_count = len(element.find_all('img', limit=5))
        if img_count > 0:
            features.append(f"{img_count} Image{'s' if img_count > 1 else ''}")
        
        btn_count = len(element.find_all(['button', 'a'], class_=lambda x: x and 'btn' in str(x)))
        if btn_count > 0:
            features.append(f"{btn_count} Button{'s' if btn_count > 1 else ''}")
        
        if features:
            return f"{category} - {', '.join(features)}"
        
        return f"{category} Section"
    
    def process_component(self, element, file_name):
        """Process and store component"""
        category = self.get_component_category(element)
        name = self.get_component_name(element, category)
        
        # Clean up the HTML
        html_str = str(element).strip()
        
        component_data = {
            'name': name,
            'html': html_str,
            'category': category,
            'source': file_name
        }
        
        self.components.append(component_data)
        self.categories[category].append(component_data)
    
    def generate_html(self):
        """Generate Tailwind UI-style component library"""
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Component Library - Tailwind Style</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #ffffff;
            color: #1f2937;
            line-height: 1.5;
        }
        
        /* Header */
        .header {
            background: white;
            border-bottom: 1px solid #e5e7eb;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .header-content {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem 2rem;
            max-width: 100%;
        }
        
        .logo {
            font-size: 1.25rem;
            font-weight: 600;
            color: #111827;
        }
        
        .breadcrumb {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #6b7280;
            font-size: 0.875rem;
        }
        
        .breadcrumb span {
            color: #d1d5db;
        }
        
        .breadcrumb a {
            color: #6b7280;
            text-decoration: none;
        }
        
        .breadcrumb a:hover {
            color: #111827;
        }
        
        .header-actions {
            display: flex;
            gap: 1rem;
            align-items: center;
        }
        
        /* View Toggle */
        .view-toggle {
            display: flex;
            background: #f3f4f6;
            border-radius: 0.375rem;
            padding: 0.125rem;
        }
        
        .view-btn {
            padding: 0.5rem 1rem;
            background: transparent;
            border: none;
            border-radius: 0.25rem;
            cursor: pointer;
            font-size: 0.875rem;
            font-weight: 500;
            color: #6b7280;
            transition: all 0.2s;
        }
        
        .view-btn.active {
            background: white;
            color: #111827;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        
        /* Layout */
        .container {
            display: flex;
            height: calc(100vh - 65px);
        }
        
        /* Sidebar */
        .sidebar {
            width: 260px;
            background: #f9fafb;
            border-right: 1px solid #e5e7eb;
            overflow-y: auto;
            flex-shrink: 0;
        }
        
        .sidebar-header {
            padding: 1.5rem 1rem 1rem;
            border-bottom: 1px solid #e5e7eb;
        }
        
        .search-box {
            width: 100%;
            padding: 0.5rem 0.75rem;
            border: 1px solid #d1d5db;
            border-radius: 0.375rem;
            font-size: 0.875rem;
            outline: none;
        }
        
        .search-box:focus {
            border-color: #6366f1;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }
        
        .category-list {
            padding: 0.5rem 0;
        }
        
        .category-item {
            padding: 0.75rem 1rem;
            cursor: pointer;
            font-size: 0.875rem;
            color: #4b5563;
            transition: all 0.2s;
            border-left: 3px solid transparent;
        }
        
        .category-item:hover {
            background: #f3f4f6;
            color: #111827;
        }
        
        .category-item.active {
            background: #eef2ff;
            color: #4f46e5;
            border-left-color: #4f46e5;
            font-weight: 500;
        }
        
        .category-count {
            float: right;
            background: #e5e7eb;
            padding: 0.125rem 0.5rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            color: #6b7280;
        }
        
        .category-item.active .category-count {
            background: #c7d2fe;
            color: #4f46e5;
        }
        
        /* Main Content */
        .main-content {
            flex: 1;
            overflow-y: auto;
            background: white;
        }
        
        /* Component Grid */
        .component-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 2rem;
            padding: 2rem;
        }
        
        .component-card {
            border: 1px solid #e5e7eb;
            border-radius: 0.5rem;
            overflow: hidden;
            transition: all 0.2s;
            cursor: pointer;
            background: white;
        }
        
        .component-card:hover {
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        
        .component-preview {
            padding: 1.5rem;
            background: #f9fafb;
            min-height: 200px;
            max-height: 300px;
            overflow: hidden;
            position: relative;
        }
        
        .component-preview::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 40px;
            background: linear-gradient(transparent, #f9fafb);
        }
        
        .component-info {
            padding: 1rem 1.5rem;
            border-top: 1px solid #e5e7eb;
        }
        
        .component-name {
            font-size: 0.875rem;
            font-weight: 500;
            color: #111827;
            margin-bottom: 0.25rem;
        }
        
        .component-source {
            font-size: 0.75rem;
            color: #9ca3af;
        }
        
        /* Full View */
        .full-view {
            display: none;
            padding: 2rem;
        }
        
        .full-view.active {
            display: block;
        }
        
        .component-full {
            margin-bottom: 3rem;
            border: 1px solid #e5e7eb;
            border-radius: 0.5rem;
            overflow: hidden;
        }
        
        .component-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 1.5rem;
            background: white;
            border-bottom: 1px solid #e5e7eb;
        }
        
        .component-title {
            font-size: 1rem;
            font-weight: 500;
            color: #111827;
        }
        
        .code-toggle {
            display: flex;
            background: #f3f4f6;
            border-radius: 0.375rem;
            padding: 0.125rem;
        }
        
        .code-btn {
            padding: 0.375rem 0.75rem;
            background: transparent;
            border: none;
            border-radius: 0.25rem;
            cursor: pointer;
            font-size: 0.75rem;
            font-weight: 500;
            color: #6b7280;
            transition: all 0.2s;
        }
        
        .code-btn.active {
            background: white;
            color: #111827;
        }
        
        .component-display {
            padding: 2rem;
            background: #fafafa;
            min-height: 200px;
        }
        
        .component-code {
            display: none;
            padding: 1.5rem;
            background: #1f2937;
            color: #e5e7eb;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.875rem;
            line-height: 1.5;
            overflow-x: auto;
        }
        
        .component-code.active {
            display: block;
        }
        
        .component-display.hidden {
            display: none;
        }
        
        /* Component styles reset */
        .component-preview > *,
        .component-display > * {
            max-width: 100%;
        }
        
        /* Dark mode toggle */
        .theme-toggle {
            padding: 0.5rem;
            background: #f3f4f6;
            border: none;
            border-radius: 0.375rem;
            cursor: pointer;
            color: #6b7280;
        }
        
        .theme-toggle:hover {
            background: #e5e7eb;
            color: #111827;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div class="logo">Component Library</div>
            <div class="breadcrumb">
                <a href="#">Components</a>
                <span>›</span>
                <span id="currentCategory">All Components</span>
            </div>
            <div class="header-actions">
                <div class="view-toggle">
                    <button class="view-btn active" onclick="toggleView('grid')">Grid</button>
                    <button class="view-btn" onclick="toggleView('full')">Full Width</button>
                </div>
                <button class="theme-toggle" onclick="toggleTheme()">🌙</button>
            </div>
        </div>
    </div>
    
    <div class="container">
        <div class="sidebar">
            <div class="sidebar-header">
                <input type="text" class="search-box" placeholder="Search components..." onkeyup="searchComponents(this.value)">
            </div>
            <div class="category-list">
                <div class="category-item active" onclick="filterCategory('all')">
                    All Components
                    <span class="category-count">''' + str(len(self.components)) + '''</span>
                </div>'''
        
        # Add categories
        for category, components in sorted(self.categories.items()):
            html += f'''
                <div class="category-item" onclick="filterCategory('{category}')">
                    {category}
                    <span class="category-count">{len(components)}</span>
                </div>'''
        
        html += '''
            </div>
        </div>
        
        <div class="main-content">
            <div class="component-grid active" id="gridView">'''
        
        # Add component cards
        for component in self.components:
            escaped_html = component['html'].replace("'", "\\'").replace('\n', '\\n')
            html += f'''
                <div class="component-card" data-category="{component['category']}" data-name="{component['name'].lower()}" onclick="openComponent('{component['category']}', '{component['name']}', '{escaped_html}')">
                    <div class="component-preview">
                        {component['html']}
                    </div>
                    <div class="component-info">
                        <div class="component-name">{component['name']}</div>
                        <div class="component-source">{component['source']}</div>
                    </div>
                </div>'''
        
        html += '''
            </div>
            
            <div class="full-view" id="fullView">'''
        
        # Add full-width components
        for component in self.components:
            html += f'''
                <div class="component-full" data-category="{component['category']}" data-name="{component['name'].lower()}">
                    <div class="component-header">
                        <div class="component-title">{component['name']}</div>
                        <div class="code-toggle">
                            <button class="code-btn active" onclick="toggleCode(this, 'preview')">Preview</button>
                            <button class="code-btn" onclick="toggleCode(this, 'code')">Code</button>
                        </div>
                    </div>
                    <div class="component-display">
                        {component['html']}
                    </div>
                    <pre class="component-code"><code>{self.escape_html(component['html'])}</code></pre>
                </div>'''
        
        html += '''
            </div>
        </div>
    </div>
    
    <script>
        let currentView = 'grid';
        let currentCategory = 'all';
        
        function toggleView(view) {
            currentView = view;
            document.querySelectorAll('.view-btn').forEach(btn => {
                btn.classList.toggle('active', btn.textContent.toLowerCase() === view);
            });
            
            document.getElementById('gridView').classList.toggle('active', view === 'grid');
            document.getElementById('fullView').classList.toggle('active', view === 'full');
        }
        
        function filterCategory(category) {
            currentCategory = category;
            
            // Update sidebar
            document.querySelectorAll('.category-item').forEach(item => {
                item.classList.toggle('active', 
                    item.textContent.includes(category === 'all' ? 'All Components' : category));
            });
            
            // Update breadcrumb
            document.getElementById('currentCategory').textContent = 
                category === 'all' ? 'All Components' : category;
            
            // Filter components
            document.querySelectorAll('.component-card, .component-full').forEach(card => {
                if (category === 'all') {
                    card.style.display = '';
                } else {
                    card.style.display = card.dataset.category === category ? '' : 'none';
                }
            });
        }
        
        function searchComponents(query) {
            query = query.toLowerCase();
            document.querySelectorAll('.component-card, .component-full').forEach(card => {
                const name = card.dataset.name;
                const category = card.dataset.category.toLowerCase();
                const matches = name.includes(query) || category.includes(query);
                card.style.display = matches ? '' : 'none';
            });
        }
        
        function toggleCode(button, view) {
            const container = button.closest('.component-full');
            const preview = container.querySelector('.component-display');
            const code = container.querySelector('.component-code');
            
            button.parentElement.querySelectorAll('.code-btn').forEach(btn => {
                btn.classList.toggle('active', btn === button);
            });
            
            if (view === 'code') {
                preview.classList.add('hidden');
                code.classList.add('active');
            } else {
                preview.classList.remove('hidden');
                code.classList.remove('active');
            }
        }
        
        function toggleTheme() {
            // Simple theme toggle - can be enhanced
            document.body.style.background = 
                document.body.style.background === 'rgb(17, 24, 39)' ? '#ffffff' : '#111827';
            document.body.style.color = 
                document.body.style.color === 'rgb(229, 231, 235)' ? '#1f2937' : '#e5e7eb';
        }
        
        function openComponent(category, name, html) {
            // Could open in modal or switch to full view
            toggleView('full');
            filterCategory(category);
            
            // Scroll to component
            setTimeout(() => {
                const component = Array.from(document.querySelectorAll('.component-full'))
                    .find(c => c.dataset.name === name.toLowerCase());
                if (component) {
                    component.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }, 100);
        }
    </script>
</body>
</html>'''
        return html
    
    def escape_html(self, html):
        """Escape HTML for display in code blocks"""
        return html.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    def save_library(self, output_file='component-library-tailwind.html'):
        """Save the component library to file"""
        output_path = os.path.join(self.folder_path, output_file)
        html_content = self.generate_html()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Component library saved to {output_file}")
        print(f"📊 Total components: {len(self.components)}")
        print(f"📁 Categories: {len(self.categories)}")
        for category, components in sorted(self.categories.items()):
            print(f"   - {category}: {len(components)} components")

if __name__ == "__main__":
    folder_path = "/Users/ryanpederson/Downloads/rumrivercomponents/New Folder With Items"
    
    extractor = TailwindStyleExtractor(folder_path)
    extractor.extract_all_components()
    extractor.save_library()