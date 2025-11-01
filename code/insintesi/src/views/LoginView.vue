<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-50 to-blue-50 px-4">
    <div
      class="bg-white/80 backdrop-blur-md shadow-xl rounded-2xl p-8 max-w-md w-full border border-gray-200 text-center"
    >
      <h2 class="text-3xl font-bold text-blue-600 mb-2">inSintesi</h2>
      <p class="text-gray-600 mb-6">Login to access your dashboard</p>

      <!-- Username -->
      <input
        v-model="username"
        type="text"
        placeholder="Email or username"
        class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-4 focus:ring-2 focus:ring-blue-500 focus:outline-none"
      />

      <!-- Password -->
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-6 focus:ring-2 focus:ring-blue-500 focus:outline-none"
      />

      <!-- Submit -->
      <button
        @click="handleLogin"
        :disabled="loading"
        class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-60"
      >
        <span v-if="loading">Logging in...</span>
        <span v-else>Login</span>
      </button>

      <!-- Error -->
      <p v-if="errorMessage" class="text-red-500 text-sm mt-4">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/authStore"

const auth = useAuthStore()
const router = useRouter()

const username = ref("")
const password = ref("")
const loading = ref(false)
const errorMessage = ref("")

const handleLogin = async () => {
  if (!username.value.trim() || !password.value.trim()) {
    errorMessage.value = "Please fill in all fields."
    return
  }

  errorMessage.value = ""
  loading.value = true

  try {
    await auth.login(username.value.trim(), password.value.trim())
    router.push("/dashboard") // Redirect post-login
  } catch (err: any) {
    console.error("Login error:", err)
    errorMessage.value = "Invalid username or password."
  } finally {
    loading.value = false
  }
}
</script>
