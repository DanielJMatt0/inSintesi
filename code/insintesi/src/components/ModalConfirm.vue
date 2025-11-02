<template>
  <teleport to="body">
    <div v-if="modelValue" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-2xl p-6 max-w-sm w-full">
        <h3 class="text-xl font-semibold text-gray-800 mb-4">{{ title }}</h3>
        <p class="text-gray-600 mb-6">{{ message }}</p>
        <div class="flex justify-end gap-2">
          <button @click="cancel" class="px-4 py-2 rounded-lg border text-gray-600 hover:bg-gray-100 transition">
            Cancel
          </button>
          <button @click="confirm" class="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition">
            Confirm
          </button>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script lang="ts" setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps<{
  modelValue: boolean
  title: string
  message: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'confirmed'): void
}>()

function cancel() {
  emit('update:modelValue', false)
}
function confirm() {
  emit('confirmed')
  emit('update:modelValue', false)
}
</script>

<style scoped>
/* Nessuna modifica extra necessaria */
</style>
