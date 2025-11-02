<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-50 to-blue-50 px-4"
  >
    <div
      class="bg-white/80 backdrop-blur-md shadow-xl rounded-2xl p-8 max-w-md w-full border border-gray-200 text-center"
    >
      <h2 class="text-3xl font-bold text-blue-600 mb-2">inSintesi</h2>
      <p class="text-gray-600 mb-6">Register as a Team Leader</p>

      <!-- Name -->
      <input
        v-model="name"
        type="text"
        placeholder="First name"
        class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-4 focus:ring-2 focus:ring-blue-500 focus:outline-none"
      />

      <!-- Lastname -->
      <input
        v-model="lastname"
        type="text"
        placeholder="Last name"
        class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-4 focus:ring-2 focus:ring-blue-500 focus:outline-none"
      />

      <!-- Email -->
      <input
        v-model="email"
        type="email"
        placeholder="Email address"
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
        @click="handleRegister"
        :disabled="loading"
        class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-60"
      >
        <span v-if="loading">Creating account...</span>
        <span v-else>Register</span>
      </button>

      <!-- Generic Error -->
      <p v-if="error" class="text-red-500 text-sm mt-4">
        Unable to register, please try again.
      </p>

      <!-- Link to login -->
      <p class="text-gray-600 text-sm mt-6">
        Already have an account?
        <router-link to="/login" class="text-blue-600 hover:underline">
          Log in
        </router-link>
      </p>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { registerTeamLead } from "@/api/auth"

const router = useRouter()

const name = ref("")
const lastname = ref("")
const email = ref("")
const password = ref("")

const loading = ref(false)
const error = ref(false)

const handleRegister = async () => {
  // Simple form validation
  if (!name.value || !lastname.value || !email.value || !password.value) {
    error.value = true
    return
  }

  loading.value = true
  error.value = false

  try {
    await registerTeamLead({
      name: name.value.trim(),
      lastname: lastname.value.trim(),
      email: email.value.trim(),
      password: password.value.trim(),
    })

    router.push("/dashboard") // Redirect after successful registration
  } catch (err) {
    console.error("Registration error:", err)
    error.value = true
  } finally {
    loading.value = false
  }
}
</script>
