<template>
  <teleport to="body">
    <transition name="fade-scale">
      <div
        v-if="modelValue"
        class="fixed inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm z-50"
      >
        <div
          class="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md text-center border border-gray-100"
        >
          <h3 class="text-2xl font-semibold text-blue-600 mb-4">
            Access Token
          </h3>
          <p class="text-gray-600 mb-6">
            Share this token with participants to allow them to answer this question.
          </p>

          <div
            class="bg-blue-50 border border-blue-200 text-blue-700 font-mono text-lg rounded-lg px-6 py-4 mb-4 select-all break-all"
          >
            {{ token }}
          </div>

          <button
            @click="copyToken"
            class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition mb-2"
          >
            Copy Token
          </button>

          <button
            @click="$emit('update:modelValue', false)"
            class="w-full border border-gray-300 text-gray-600 py-2 rounded-lg hover:bg-gray-100 transition"
          >
            Close
          </button>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script lang="ts" setup>
const props = defineProps<{
  modelValue: boolean
  token: string
}>()

const emit = defineEmits(["update:modelValue"])

const copyToken = async () => {
  await navigator.clipboard.writeText(props.token)
  emit("update:modelValue", false)
}
</script>

<style scoped>
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: all 0.25s ease;
}
.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>
