<template>
  <section class="hero-split">
    <div class="hero-content">
      <h1>{{ title }}</h1>
      <p>{{ description }}</p>
      <div class="btn-group">
        <button class="btn btn-primary">{{ primaryBtnText }}</button>
        <button class="btn btn-link">{{ secondaryBtnText }} →</button>
      </div>
    </div>
    <div class="hero-image">
      <img v-if="imageUrl" :src="imageUrl" :alt="title">
      <div v-else class="image-placeholder">
        {{ imagePlaceholder }}
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'HeroSplit',
  props: {
    title: {
      type: String,
      default: 'Deploy to the cloud with confidence'
    },
    description: {
      type: String,
      default: 'Anim aute id magna aliqua ad ad non deserunt sunt. Qui irure qui lorem cupidatat commodo. Elit sunt amet fugiat veniam occaecat fugiat aliqua.'
    },
    primaryBtnText: {
      type: String,
      default: 'Get started'
    },
    secondaryBtnText: {
      type: String,
      default: 'Live demo'
    },
    imageUrl: {
      type: String,
      default: ''
    },
    imagePlaceholder: {
      type: String,
      default: '[Image Placeholder]'
    }
  }
}
</script>

<style scoped>
.hero-split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  padding: 4rem 2rem;
  align-items: center;
  min-height: 500px;
}

.hero-content h1 {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #111827;
}

.hero-content p {
  font-size: 1.125rem;
  color: #6b7280;
  margin-bottom: 2rem;
  line-height: 1.75;
}

.btn-group {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.btn-link {
  background: transparent;
  border: none;
  color: #4f46e5;
  padding: 0.625rem 0;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
}

.btn-link:hover {
  color: #4338ca;
}

.hero-image {
  width: 100%;
  height: 100%;
  min-height: 400px;
}

.image-placeholder {
  width: 100%;
  height: 400px;
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  font-size: 1.125rem;
}

.hero-image img {
  width: 100%;
  height: auto;
  border-radius: 0.5rem;
}
</style>