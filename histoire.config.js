import { defineConfig } from 'histoire'
import { HstVue } from '@histoire/plugin-vue'

export default defineConfig({
  plugins: [
    HstVue()
  ],
  setupFile: './src/histoire-setup.js',
  theme: {
    title: 'Component Library'
  },
  tree: {
    groups: [
      {
        id: 'heroes',
        title: 'Heroes',
        include: story => story.title.startsWith('Heroes/')
      },
      {
        id: 'features',
        title: 'Features',
        include: story => story.title.startsWith('Features/')
      },
      {
        id: 'content',
        title: 'Content Sections',
        include: story => story.title.startsWith('Content/')
      },
      {
        id: 'cta',
        title: 'CTA Sections',
        include: story => story.title.startsWith('Cta/')
      },
      {
        id: 'testimonials',
        title: 'Testimonials',
        include: story => story.title.startsWith('Testimonials/')
      },
      {
        id: 'pricing',
        title: 'Pricing',
        include: story => story.title.startsWith('Pricing/')
      },
      {
        id: 'contact',
        title: 'Contact',
        include: story => story.title.startsWith('Contact/')
      },
      {
        id: 'navigation',
        title: 'Navigation',
        include: story => story.title.startsWith('Navigation/')
      },
      {
        id: 'footers',
        title: 'Footers',
        include: story => story.title.startsWith('Footers/')
      }
    ],
    order: 'asc'
  },
  defaultStoryProps: {
    layout: {
      type: 'grid',
      width: '100%'
    }
  }
})