<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-50 to-blue-50">
    <div
      class="bg-white/80 backdrop-blur-md shadow-xl rounded-2xl p-8 max-w-md w-full text-center border border-gray-200"
    >
      <h2 class="text-3xl font-bold text-blue-600 mb-3">inSintesi</h2>
      <p class="text-gray-600 mb-6">
        Enter your access token or scan a QR code to participate.
      </p>

      <!-- TOKEN INPUT -->
      <input
        v-model="token"
        type="text"
        placeholder="Enter your token"
        class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-4 focus:ring-2 focus:ring-blue-500 focus:outline-none"
      />

      <button
        @click="handleManualLogin"
        class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition mb-4 disabled:opacity-50"
        :disabled="loading"
      >
        {{ loading ? "Checking..." : "Enter" }}
      </button>

      <p v-if="errorMessage" class="text-red-500 text-sm mb-3">{{ errorMessage }}</p>

      <div class="flex items-center justify-center mb-3">
        <div class="border-t border-gray-300 w-1/3"></div>
        <span class="text-sm text-gray-400 px-2">or</span>
        <div class="border-t border-gray-300 w-1/3"></div>
      </div>

      <!-- QR SCANNER BUTTON -->
      <button
        @click="toggleCamera"
        class="w-full bg-gray-100 border border-gray-300 py-2 rounded-lg hover:bg-gray-200 transition mb-4"
      >
        <span v-if="!scanning">Scan QR Code</span>
        <span v-else>Stop Scanning</span>
      </button>

      <transition name="fade">
        <div v-if="scanning" class="mt-6">
          <qrcode-stream @detect="onDetect" @error="onError" />
          <p class="text-sm text-gray-500 mt-2">Point your camera at the QR code</p>
        </div>
      </transition>

      <!-- LOGIN BUTTON -->
      <div class="mt-6">
        <button
          @click="goToLogin"
          class="w-full border border-blue-500 text-blue-600 py-2 rounded-lg hover:bg-blue-50 transition"
        >
          Login as Team Lead
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { QrcodeStream } from "vue-qrcode-reader"
import { getQuestionFromToken } from "@/api/answer"

const router = useRouter()
const token = ref("")
const loading = ref(false)
const errorMessage = ref("")
const scanning = ref(false)

const toggleCamera = () => (scanning.value = !scanning.value)

/**
 * Check the validity of the token
 */
const checkTokenValidity = async (tokenValue: string): Promise<boolean> => {
  try {
    loading.value = true
    errorMessage.value = ""
    await getQuestionFromToken(tokenValue)
    return true
  } catch (err: any) {
    console.error("Token check failed:", err)
    errorMessage.value = "Invalid or expired token."
    return false
  } finally {
    loading.value = false
  }
}

/**
 * Manual login (using token with input)
 */
const handleManualLogin = async () => {
  const trimmed = token.value.trim()
  if (!trimmed) {
    errorMessage.value = "Please enter a valid token."
    return
  }

  const valid = await checkTokenValidity(trimmed)
  if (valid) router.push(`/respond/${trimmed}`)
}

/**
 * Login using QR code (contains token)
 */
const onDetect = async (detectedCodes: any[]) => {
  if (!detectedCodes.length) return

  // Closes camera
  scanning.value = false

  // QR value
  const scannedToken = detectedCodes[0].rawValue?.trim()
  if (!scannedToken) {
    errorMessage.value = "No token found in QR code."
    return
  }

  // Shows token in input
  token.value = scannedToken

  // Checks token validity
  const valid = await checkTokenValidity(scannedToken)
  if (valid) {
    router.push(`/respond/${scannedToken}`)
  } else {
    errorMessage.value = "Invalid or expired token."
  }
}

const onError = (error: any) => {
  console.error("QR scan error:", error)
  alert("Unable to access camera. Please check permissions.")
}

// Redirect to login page
const goToLogin = () => {
  router.push("/login")
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
