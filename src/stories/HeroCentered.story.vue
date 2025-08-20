<script setup>
import HeroCentered from '../components/HeroCentered.vue'
</script>

<template>
  <Story 
    title="Heroes/Centered with Badge" 
    :layout="{ type: 'single', iframe: true }"
  >
    <Variant title="Default with Email">
      <HeroCentered />
    </Variant>
    
    <Variant title="Product Launch">
      <HeroCentered 
        badge="New Product Launch"
        title="Introducing our newest innovation"
        description="Experience the future of productivity with our revolutionary platform that transforms how teams work together."
        cta-text="Join waitlist"
        :show-email-input="true"
        email-placeholder="Enter your work email"
        disclaimer="No spam, unsubscribe at any time."
      />
    </Variant>
    
    <Variant title="Without Email Input">
      <HeroCentered 
        badge="Limited Time Offer"
        title="Transform your workflow today"
        description="Join thousands of companies already using our platform to increase productivity and drive growth."
        cta-text="Start free trial"
        :show-email-input="false"
      />
    </Variant>
    
    <Variant title="Conference">
      <HeroCentered 
        badge="June 15-17, 2024 • San Francisco"
        title="The conference for modern developers"
        description="Join us for three days of talks, workshops, and networking with the best minds in tech."
        cta-text="Register now"
        :show-email-input="false"
        disclaimer=""
      />
    </Variant>
  </Story>
</template>