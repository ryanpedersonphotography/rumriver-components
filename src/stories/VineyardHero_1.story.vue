<script setup>
import VineyardHero_1 from '../components/VineyardHero_1.vue'
</script>

<template>
  <Story 
    title="Heroes/VineyardHero 1" 
    :layout="{ type: 'single', iframe: true }"
  >
    <Variant title="Default">
      <VineyardHero_1 />
    </Variant>
  </Story>
</template>