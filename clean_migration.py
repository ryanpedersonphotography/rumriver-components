#!/usr/bin/env python3
"""
Clean migration script - removes duplicates and improves naming
"""

import os
import re
import hashlib
from bs4 import BeautifulSoup
from collections import defaultdict
import shutil

class ComponentCleaner:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.components_dir = os.path.join(folder_path, 'src', 'components')
        self.stories_dir = os.path.join(folder_path, 'src', 'stories')
        
    def clean_existing_components(self):
        """Remove duplicate and poorly named components"""
        # Get all existing component files
        if not os.path.exists(self.components_dir):
            print("No components directory found")
            return
            
        component_files = [f for f in os.listdir(self.components_dir) if f.endswith('.vue')]
        story_files = [f for f in os.listdir(self.stories_dir) if f.endswith('.story.vue')]
        
        # Components to remove (duplicates and poorly named)
        remove_patterns = [
            r'^400AcresOf',  # Components starting with numbers
            r'Component_\d+$',  # Generic numbered components
        ]
        
        # Find duplicates by content hash
        content_hashes = {}
        components_to_keep = {}
        
        for comp_file in component_files:
            comp_path = os.path.join(self.components_dir, comp_file)
            
            # Skip if matches removal pattern
            comp_name = comp_file.replace('.vue', '')
            if any(re.match(pattern, comp_name) for pattern in remove_patterns):
                print(f"  Removing (bad name): {comp_name}")
                os.remove(comp_path)
                story_path = os.path.join(self.stories_dir, f"{comp_name}.story.vue")
                if os.path.exists(story_path):
                    os.remove(story_path)
                continue
            
            # Check for content duplicates
            with open(comp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract just the template content for comparison
                soup = BeautifulSoup(content, 'html.parser')
                template_match = re.search(r'<template>(.*?)</template>', content, re.DOTALL)
                if template_match:
                    template_content = template_match.group(1)
                    content_hash = hashlib.md5(template_content.encode()).hexdigest()
                    
                    if content_hash in content_hashes:
                        # Duplicate found
                        existing = content_hashes[content_hash]
                        # Keep the one with the better name
                        if len(comp_name) < len(existing) or comp_name < existing:
                            # Remove the existing one, keep this one
                            print(f"  Removing duplicate: {existing} (keeping {comp_name})")
                            old_comp_path = os.path.join(self.components_dir, f"{existing}.vue")
                            old_story_path = os.path.join(self.stories_dir, f"{existing}.story.vue")
                            if os.path.exists(old_comp_path):
                                os.remove(old_comp_path)
                            if os.path.exists(old_story_path):
                                os.remove(old_story_path)
                            content_hashes[content_hash] = comp_name
                        else:
                            # Remove this one
                            print(f"  Removing duplicate: {comp_name} (keeping {existing})")
                            os.remove(comp_path)
                            story_path = os.path.join(self.stories_dir, f"{comp_name}.story.vue")
                            if os.path.exists(story_path):
                                os.remove(story_path)
                    else:
                        content_hashes[content_hash] = comp_name
        
        # Clean up similar named components
        self.consolidate_similar_components()
        
    def consolidate_similar_components(self):
        """Consolidate components with very similar names"""
        component_files = [f for f in os.listdir(self.components_dir) if f.endswith('.vue')]
        
        # Group by base name
        name_groups = defaultdict(list)
        for comp_file in component_files:
            comp_name = comp_file.replace('.vue', '')
            # Extract base name (without numbers at the end)
            base_name = re.sub(r'_\d+$', '', comp_name)
            name_groups[base_name].append(comp_name)
        
        # For groups with multiple similar components, keep only the first few
        for base_name, components in name_groups.items():
            if len(components) > 2:  # If more than 2 with same base name
                print(f"\n  Consolidating {base_name} components ({len(components)} found)")
                # Sort to ensure consistent ordering
                components.sort()
                # Keep first 2, remove the rest
                for comp_name in components[2:]:
                    print(f"    Removing redundant: {comp_name}")
                    comp_path = os.path.join(self.components_dir, f"{comp_name}.vue")
                    story_path = os.path.join(self.stories_dir, f"{comp_name}.story.vue")
                    if os.path.exists(comp_path):
                        os.remove(comp_path)
                    if os.path.exists(story_path):
                        os.remove(story_path)
        
    def rename_components(self):
        """Give components better names based on their content"""
        component_files = [f for f in os.listdir(self.components_dir) if f.endswith('.vue')]
        
        renames = {
            'APicturesqueSetting': 'VenueLandscape',
            'WhereRusticCharm': 'RusticHero',
            'WillowCreekbarn': 'BarnVenue',
            'RumRiverbarnVineyard': 'VineyardHero',
            'HeroeComponent': 'HeroSection',
            'WhereLoveStories': 'LoveStoryHero',
            'TheHistoricBarn': 'HistoricVenue',
            'YourperfectDayawaits': 'PerfectDayHero'
        }
        
        for comp_file in component_files:
            comp_name = comp_file.replace('.vue', '')
            
            # Check if this component should be renamed
            for old_pattern, new_base in renames.items():
                if comp_name.startswith(old_pattern):
                    # Extract any suffix
                    suffix = comp_name[len(old_pattern):]
                    if suffix and suffix[0] == '_':
                        new_name = f"{new_base}{suffix}"
                    else:
                        new_name = new_base
                    
                    if new_name != comp_name:
                        print(f"  Renaming: {comp_name} → {new_name}")
                        
                        # Rename component file
                        old_comp_path = os.path.join(self.components_dir, f"{comp_name}.vue")
                        new_comp_path = os.path.join(self.components_dir, f"{new_name}.vue")
                        
                        # Update component content
                        with open(old_comp_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        content = content.replace(f"name: '{comp_name}'", f"name: '{new_name}'")
                        content = content.replace(f'class="{comp_name.lower()}-component"', 
                                                f'class="{new_name.lower()}-component"')
                        
                        with open(new_comp_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        # Rename story file
                        old_story_path = os.path.join(self.stories_dir, f"{comp_name}.story.vue")
                        new_story_path = os.path.join(self.stories_dir, f"{new_name}.story.vue")
                        
                        if os.path.exists(old_story_path):
                            with open(old_story_path, 'r', encoding='utf-8') as f:
                                story_content = f.read()
                            story_content = story_content.replace(f"import {comp_name}", f"import {new_name}")
                            story_content = story_content.replace(f"from '../components/{comp_name}.vue'", 
                                                                f"from '../components/{new_name}.vue'")
                            story_content = story_content.replace(f"<{comp_name} />", f"<{new_name} />")
                            # Update display name in title
                            old_display = comp_name.replace('_', ' ')
                            new_display = new_name.replace('_', ' ')
                            story_content = story_content.replace(f"/{old_display}\"", f"/{new_display}\"")
                            
                            with open(new_story_path, 'w', encoding='utf-8') as f:
                                f.write(story_content)
                            
                            os.remove(old_story_path)
                        
                        os.remove(old_comp_path)
                    break
    
    def run_cleanup(self):
        """Run the full cleanup process"""
        print("🧹 Starting component cleanup...")
        print("\n📦 Removing duplicates and bad components...")
        self.clean_existing_components()
        
        print("\n✏️  Renaming components for clarity...")
        self.rename_components()
        
        # Count final components
        if os.path.exists(self.components_dir):
            final_count = len([f for f in os.listdir(self.components_dir) if f.endswith('.vue')])
            print(f"\n✅ Cleanup complete! {final_count} components remaining.")
        else:
            print("\n❌ No components found.")

if __name__ == "__main__":
    folder_path = "/Users/ryanpederson/Downloads/rumrivercomponents/New Folder With Items"
    cleaner = ComponentCleaner(folder_path)
    cleaner.run_cleanup()