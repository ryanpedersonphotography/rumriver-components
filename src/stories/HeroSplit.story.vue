<script setup>
import HeroSplit from '../components/HeroSplit.vue'
</script>

<template>
  <Story 
    title="Heroes/Split Layout" 
    :layout="{ type: 'single', iframe: true }"
  >
    <Variant title="Default">
      <HeroSplit />
    </Variant>
    
    <Variant title="Marketing">
      <HeroSplit 
        title="Grow your business online"
        description="Our platform provides everything you need to build, launch, and scale your digital presence with confidence."
        primary-btn-text="Start now"
        secondary-btn-text="See how it works"
      />
    </Variant>
    
    <Variant title="SaaS Product">
      <HeroSplit 
        title="The modern way to manage your team"
        description="Streamline workflows, enhance collaboration, and boost productivity with our all-in-one platform designed for remote teams."
        primary-btn-text="Try for free"
        secondary-btn-text="Book a demo"
      />
    </Variant>
    
    <Variant title="Developer Tools">
      <HeroSplit 
        title="Ship faster with better tools"
        description="Build, test, and deploy your applications with confidence using our developer-first platform and comprehensive API."
        primary-btn-text="Get started"
        secondary-btn-text="View docs"
      />
    </Variant>
  </Story>
</template>