<template>
  <section
    class="bg-white shadow-md rounded-2xl p-6 mb-8 border border-gray-100 transition hover:shadow-lg"
  >
    <!-- Title -->
    <header class="mb-4">
      <h2 class="text-2xl font-semibold text-gray-800">
        {{ title }}
      </h2>

      <!-- Description -->
      <p v-if="description" class="text-gray-500 mt-1">
        {{ description }}
      </p>
    </header>

    <!-- Dynamic Content -->
    <div class="mt-4">
      <slot />
    </div>
  </section>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  description: {
    // Optional
    type: String,
    default: '',
  },
})
</script>

<style scoped>
/* Hover effect */
section {
  transition:
    box-shadow 0.2s ease,
    transform 0.2s ease;
}
section:hover {
  transform: translateY(-2px);
}
</style>
