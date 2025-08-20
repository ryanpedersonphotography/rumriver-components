<script setup>
import Intimate_42 from '../components/Intimate_42.vue'
</script>

<template>
  <Story 
    title="Pricing/Intimate 42" 
    :layout="{ type: 'single', iframe: true }"
  >
    <Variant title="Default">
      <Intimate_42 />
    </Variant>
  </Story>
</template>