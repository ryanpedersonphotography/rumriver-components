<script setup>
import HeroSimple from '../components/HeroSimple.vue'
</script>

<template>
  <Story 
    title="Heroes/Simple Gradient" 
    :layout="{ type: 'single', iframe: true }"
  >
    <Variant title="Default">
      <HeroSimple />
    </Variant>
    
    <Variant title="Purple Gradient">
      <HeroSimple 
        title="Build amazing products"
        description="Create beautiful, fast and secure web applications tailored to your business needs."
        primary-btn-text="Start free trial"
        secondary-btn-text="View demo"
        bg-color="linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
      />
    </Variant>
    
    <Variant title="Blue Gradient">
      <HeroSimple 
        title="Welcome to the future"
        description="Experience the next generation of web development with our cutting-edge platform."
        bg-color="linear-gradient(135deg, #0061ff 0%, #60efff 100%)"
      />
    </Variant>
    
    <Variant title="Dark">
      <HeroSimple 
        title="Premium Components"
        description="Professional-grade UI components for modern web applications."
        bg-color="linear-gradient(135deg, #1f2937 0%, #111827 100%)"
      />
    </Variant>
  </Story>
</template>