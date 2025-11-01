<template>
  <div class="min-h-screen bg-gray-50 text-gray-800">
    <header class="bg-white shadow-md p-4 flex justify-between items-center">
      <router-link
        to="/"
        class="text-2xl font-bold hover:text-blue-600 transition"
      >
        inSintesi
      </router-link>
    </header>

    <main class="max-w-5xl mx-auto py-10 px-6">
      <router-view />
    </main>
  </div>
</template>

<script setup>
// Dynamically loaded with routing
</script>

<style>
body {
  font-family: Inter, system-ui, sans-serif;
  background-color: #f9fafb;
  margin: 0;
}
</style>
