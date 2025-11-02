<template>
  <div class="min-h-screen bg-gray-50 text-gray-800">
    <Navbar v-if="showNavbar" />

    <main class="max-w-7xl mx-auto px-6">
      <router-view />
    </main>
  </div>
</template>


<script setup lang="ts">
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import Navbar from '@/components/Navbar.vue'
const route = useRoute()
const showNavbar = computed(() => route.meta.showNavbar !== false)
</script>

<style>
body {
  font-family: Inter, system-ui, sans-serif;
  background-color: #f9fafb;
  margin: 0;
}
</style>
