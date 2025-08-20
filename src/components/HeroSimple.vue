<template>
  <section class="hero-simple" :style="{ background: bgColor }">
    <div class="hero-content">
      <h1>{{ title }}</h1>
      <p>{{ description }}</p>
      <div class="btn-group">
        <button class="btn btn-primary">{{ primaryBtnText }}</button>
        <button class="btn btn-secondary">{{ secondaryBtnText }}</button>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'HeroSimple',
  props: {
    title: {
      type: String,
      default: 'Data to enrich your online business'
    },
    description: {
      type: String,
      default: 'Anim aute id magna aliqua ad ad non deserunt sunt. Qui irure qui lorem cupidatat commodo.'
    },
    primaryBtnText: {
      type: String,
      default: 'Get started'
    },
    secondaryBtnText: {
      type: String,
      default: 'Learn more'
    },
    bgColor: {
      type: String,
      default: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    }
  }
}
</script>

<style scoped>
.hero-simple {
  padding: 6rem 2rem;
  text-align: center;
  color: white;
  min-height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-content {
  max-width: 800px;
}

.hero-simple h1 {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
}

.hero-simple p {
  font-size: 1.25rem;
  opacity: 0.95;
  margin-bottom: 2.5rem;
}

.btn-group {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.hero-simple .btn-primary {
  background: white;
  color: #667eea;
}

.hero-simple .btn-secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}
</style>