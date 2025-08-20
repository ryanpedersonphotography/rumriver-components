#!/usr/bin/env python3
"""
Migrate HTML components to Vue components and Histoire stories
"""

import os
import re
import hashlib
from bs4 import BeautifulSoup
from collections import defaultdict
import json

class HistoireMigrator:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.components = []
        self.categories = defaultdict(list)
        self.seen_hashes = set()
        self.component_count = 0
        
    def extract_all_components(self):
        """Extract components from all HTML files"""
        html_files = [f for f in os.listdir(self.folder_path) 
                     if f.endswith('.html') and not f.startswith(('component-library', 'tailwind', 'barn-venue'))]
        
        print(f"Found {len(html_files)} HTML files to process")
        
        for file_name in html_files:
            print(f"Processing: {file_name}")
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
            selectors = [
                'section', 'header', 'footer', 'nav',
                'div.hero', 'div.feature', 'div.testimonial', 
                'div.pricing', 'div.cta', 'div.contact',
                '[class*="hero"]', '[class*="feature"]', '[class*="testimonial"]',
                '[class*="pricing"]', '[class*="cta"]', '[class*="banner"]',
                'div.container > div', 'main > div'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)[:3]  # Limit per selector to avoid too many similar components
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
        if len(text_content) < 30:  # Minimum content threshold
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
        classes = ' '.join(element.get('class', [])) if element.get('class') else ''
        tag = element.name
        text = element.get_text(strip=True).lower()
        
        # Category detection logic
        if tag == 'nav' or 'nav' in classes or 'navigation' in classes:
            return "navigation"
        elif tag == 'header' or 'header' in classes or 'hero' in classes or 'hero' in text[:100]:
            return "heroes"
        elif tag == 'footer' or 'footer' in classes:
            return "footers"
        elif 'testimonial' in classes or 'testimonial' in text or 'review' in text:
            return "testimonials"
        elif 'pricing' in classes or 'price' in text or 'plan' in text:
            return "pricing"
        elif 'feature' in classes or 'service' in classes or 'feature' in text[:100]:
            return "features"
        elif 'cta' in classes or 'call-to-action' in text or 'get started' in text:
            return "cta"
        elif 'contact' in classes or 'contact' in text or 'email' in text:
            return "contact"
        elif 'blog' in classes or 'article' in classes or 'post' in classes:
            return "content"
        else:
            return "content"
    
    def sanitize_component_name(self, name):
        """Sanitize name for use as Vue component name"""
        # Remove special characters and convert to PascalCase
        name = re.sub(r'[^\w\s]', '', name)
        name = re.sub(r'\s+', ' ', name)
        words = name.split()[:3]  # Limit to 3 words
        return ''.join(word.capitalize() for word in words)
    
    def get_component_name(self, element, category, index):
        """Generate a unique component name"""
        # Try to get a meaningful name from headings
        heading = element.find(['h1', 'h2', 'h3'])
        if heading:
            name = self.sanitize_component_name(heading.get_text(strip=True))
            if name:
                return f"{name}_{index}"
        
        # Count key elements for naming
        img_count = len(element.find_all('img', limit=5))
        btn_count = len(element.find_all(['button', 'a'], class_=lambda x: x and 'btn' in str(x)))
        
        # Generate descriptive name
        base_name = category.capitalize().rstrip('s')
        features = []
        
        if img_count > 0:
            features.append(f"{img_count}Img")
        if btn_count > 0:
            features.append(f"{btn_count}Btn")
        
        if features:
            return f"{base_name}{''.join(features)}_{index}"
        
        return f"{base_name}Component_{index}"
    
    def create_vue_component(self, component_data):
        """Create a Vue component file from component data"""
        template = f"""<template>
  <div class="{component_data['name'].lower()}-component">
{component_data['html']}
  </div>
</template>

<script>
export default {{
  name: '{component_data['name']}',
  props: {{
    // Add props as needed
  }}
}}
</script>

<style scoped>
/* Component-specific styles */
</style>"""
        return template
    
    def create_histoire_story(self, component_data):
        """Create a Histoire story file for the component"""
        story = f"""<script setup>
import {component_data['name']} from '../components/{component_data['name']}.vue'
</script>

<template>
  <Story 
    title="{component_data['category'].capitalize()}/{component_data['display_name']}" 
    :layout="{{ type: 'single', iframe: true }}"
  >
    <Variant title="Default">
      <{component_data['name']} />
    </Variant>
  </Story>
</template>"""
        return story
    
    def process_component(self, element, file_name):
        """Process and store component"""
        self.component_count += 1
        category = self.get_component_category(element)
        name = self.get_component_name(element, category, self.component_count)
        
        # Clean up the HTML - indent it properly
        soup = BeautifulSoup(str(element), 'html.parser')
        pretty_html = soup.prettify()
        
        # Indent the HTML for Vue template
        lines = pretty_html.split('\n')
        indented_html = '\n'.join('    ' + line if line.strip() else '' for line in lines)
        
        component_data = {
            'name': name,
            'display_name': name.replace('_', ' '),
            'html': indented_html,
            'category': category,
            'source': file_name
        }
        
        self.components.append(component_data)
        self.categories[category].append(component_data)
    
    def save_components(self):
        """Save all Vue components and Histoire stories"""
        components_dir = os.path.join(self.folder_path, 'src', 'components')
        stories_dir = os.path.join(self.folder_path, 'src', 'stories')
        
        # Ensure directories exist
        os.makedirs(components_dir, exist_ok=True)
        os.makedirs(stories_dir, exist_ok=True)
        
        print(f"\n📦 Saving {len(self.components)} components...")
        
        # Save each component and its story
        for component in self.components:
            # Save Vue component
            component_path = os.path.join(components_dir, f"{component['name']}.vue")
            with open(component_path, 'w', encoding='utf-8') as f:
                f.write(self.create_vue_component(component))
            
            # Save Histoire story
            story_path = os.path.join(stories_dir, f"{component['name']}.story.vue")
            with open(story_path, 'w', encoding='utf-8') as f:
                f.write(self.create_histoire_story(component))
        
        print(f"✅ Components saved to {components_dir}")
        print(f"📚 Stories saved to {stories_dir}")
        
        # Print summary
        print(f"\n📊 Migration Summary:")
        print(f"   Total components: {len(self.components)}")
        print(f"   Categories: {len(self.categories)}")
        for category, components in sorted(self.categories.items()):
            print(f"   - {category}: {len(components)} components")

if __name__ == "__main__":
    folder_path = "/Users/ryanpederson/Downloads/rumrivercomponents/New Folder With Items"
    
    migrator = HistoireMigrator(folder_path)
    migrator.extract_all_components()
    
    # Limit to reasonable number of components for initial test
    if len(migrator.components) > 50:
        print(f"\n⚠️  Found {len(migrator.components)} components. Limiting to first 50 for initial migration.")
        migrator.components = migrator.components[:50]
        
        # Rebuild categories with limited components
        migrator.categories = defaultdict(list)
        for comp in migrator.components:
            migrator.categories[comp['category']].append(comp)
    
    migrator.save_components()