<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-50 to-blue-50 px-4">
    <div class="bg-white/80 backdrop-blur-md shadow-xl rounded-2xl p-8 max-w-md w-full border border-gray-200 text-center">
      <h2 class="text-3xl font-bold text-green-600 mb-4">🎉 Thank you!</h2>
      <p class="text-gray-700 mb-6">
        Your answer has been submitted successfully.
      </p>

      <div class="flex justify-center space-x-4">
        <button
          @click="goHome"
          class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
        >
          Go to Home
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useRouter } from "vue-router"
const router = useRouter()

const goHome = () => {
  router.push("/")
}
</script>
