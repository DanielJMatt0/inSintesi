<template>
  <div class="bg-white shadow-md rounded-xl p-5 hover:shadow-lg transition">
    <h3 class="text-lg font-semibold">{{ topic.title }}</h3>
    <p class="text-sm text-gray-600 mt-1">{{ topic.description }}</p>

    <div class="flex justify-between items-center mt-3">
      <span class="text-xs text-gray-500">Responses: {{ topic.responses }}</span>
      <button @click="$emit('remove')" class="text-red-500 hover:text-red-700 text-sm">
        Remove
      </button>
    </div>
  </div>
</template>

<script lang="ts" setup>
defineProps({
  topic: {
    type: Object,
    required: true,
  },
});
</script>
