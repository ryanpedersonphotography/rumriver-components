<template>
  <section class="hero-centered">
    <div class="hero-container">
      <span v-if="badge" class="badge">{{ badge }}</span>
      <h1>{{ title }}</h1>
      <p>{{ description }}</p>
      <div class="cta-section">
        <input 
          v-if="showEmailInput"
          type="email" 
          class="email-input" 
          :placeholder="emailPlaceholder"
          v-model="email"
        >
        <button class="btn btn-primary">{{ ctaText }}</button>
      </div>
      <p v-if="disclaimer" class="disclaimer">{{ disclaimer }}</p>
    </div>
  </section>
</template>

<script>
export default {
  name: 'HeroCentered',
  props: {
    badge: {
      type: String,
      default: 'Announcing our next round of funding'
    },
    title: {
      type: String,
      default: 'Data to enrich your online business'
    },
    description: {
      type: String,
      default: 'Anim aute id magna aliqua ad ad non deserunt sunt. Qui irure qui lorem cupidatat commodo. Elit sunt amet fugiat veniam occaecat fugiat aliqua.'
    },
    ctaText: {
      type: String,
      default: 'Get started'
    },
    showEmailInput: {
      type: Boolean,
      default: true
    },
    emailPlaceholder: {
      type: String,
      default: 'Enter your email'
    },
    disclaimer: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      email: ''
    }
  }
}
</script>

<style scoped>
.hero-centered {
  padding: 6rem 2rem;
  text-align: center;
  background: white;
}

.hero-container {
  max-width: 900px;
  margin: 0 auto;
}

.badge {
  display: inline-block;
  background: #eef2ff;
  color: #4f46e5;
  padding: 0.375rem 1rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 1.5rem;
}

.hero-centered h1 {
  font-size: 4rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #111827 0%, #4f46e5 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-centered p {
  font-size: 1.25rem;
  color: #6b7280;
  margin-bottom: 2.5rem;
  line-height: 1.75;
}

.cta-section {
  display: flex;
  gap: 1rem;
  max-width: 500px;
  margin: 0 auto 1rem;
  justify-content: center;
}

.email-input {
  flex: 1;
  padding: 0.875rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 1rem;
  outline: none;
}

.email-input:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.disclaimer {
  font-size: 0.875rem;
  color: #9ca3af;
  margin-top: 1rem;
}
</style>