<template>
    <div class="min-h-screen flex flex-col justify-between bg-gradient-to-br from-gray-50 to-blue-50 relative">
        <!-- DASHBOARD LOGIN BUTTON -->
        <button @click="showAdminLogin = true"
            class="absolute top-4 right-6 text-sm text-gray-600 hover:text-blue-600 border border-transparent hover:border-blue-300 rounded-lg px-3 py-1 transition">
            Dashboard
        </button>

        <!-- MAIN CONTENT -->
        <main class="flex flex-col items-center justify-center flex-grow px-4">
            <div
                class="bg-white/80 backdrop-blur-md shadow-xl rounded-2xl p-8 max-w-md w-full text-center border border-gray-200">
                <h2 class="text-3xl font-bold text-blue-600 mb-3">inSintesi</h2>
                <p class="text-gray-600 mb-6">
                    Harness the collective wisdom of your team with AI-driven consensus to make smarter, faster and more
                    inclusive decisions.
                </p>

                <!-- TOKEN INPUT -->
                <input v-model="token" type="text" placeholder="Enter your token"
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-4 focus:ring-2 focus:ring-blue-500 focus:outline-none" />

                <button @click="handleManualLogin"
                    class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition mb-3">
                    Enter
                </button>

                <div class="flex items-center justify-center mb-3">
                    <div class="border-t border-gray-300 w-1/3"></div>
                    <span class="text-sm text-gray-400 px-2">or</span>
                    <div class="border-t border-gray-300 w-1/3"></div>
                </div>

                <!-- QR SCANNER -->
                <button @click="toggleCamera"
                    class="w-full bg-gray-100 border border-gray-300 py-2 rounded-lg hover:bg-gray-200 transition">
                    <span v-if="!scanning">📷 Scan QR Code</span>
                    <span v-else>❌ Stop Scanning</span>
                </button>

                <transition name="fade">
                    <div v-if="scanning" class="mt-6">
                        <qrcode-stream @detect="onDetect" @error="onError" />
                        <p class="text-sm text-gray-500 mt-2">Point your camera at the QR code</p>
                    </div>
                </transition>
            </div>
        </main>

        <!-- FOOTER -->
        <footer
            class="border-t border-gray-200 py-5 px-9 flex flex-col sm:flex-row justify-between items-center text-gray-600 text-sm">
            <p>© 2025 inSintesi. All rights reserved.</p>
            <div class="flex space-x-4 mt-2 sm:mt-0">
                <a href="#" class="hover:text-blue-600">Privacy Policy</a>
                <a href="#" class="hover:text-blue-600">Terms of Use</a>
                <a href="#" class="hover:text-blue-600">Contact</a>
                <div class="flex space-x-2 ml-2">
                    <a href="#" class="hover:text-blue-600">🌐</a>
                    <a href="#" class="hover:text-blue-600">🐦</a>
                    <a href="#" class="hover:text-blue-600">💼</a>
                </div>
            </div>
        </footer>

        <!-- ADMIN LOGIN MODAL -->
        <transition name="fade">
            <div v-if="showAdminLogin"
                class="fixed inset-0 flex items-center justify-center bg-gray-900/30 backdrop-blur-sm z-50"
                @click.self="showAdminLogin = false">
                <transition name="scale">
                    <div v-if="showAdminLogin"
                        class="bg-white rounded-xl p-6 shadow-2xl w-full max-w-sm border border-gray-100">
                        <h3 class="text-xl font-semibold mb-4 text-center text-gray-800">Dashboard login</h3>
                        <input v-model="admin.username" type="text" placeholder="Username"
                            class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-3 focus:ring-2 focus:ring-blue-500" />
                        <input v-model="admin.password" type="password" placeholder="Password"
                            class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-4 focus:ring-2 focus:ring-blue-500" />
                        <div class="flex justify-end space-x-3">
                            <button @click="showAdminLogin = false"
                                class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-100">
                                Cancel
                            </button>
                            <button @click="handleAdminLogin"
                                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                                Enter
                            </button>
                        </div>
                    </div>
                </transition>
            </div>
        </transition>
    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { QrcodeStream } from 'vue-qrcode-reader'

const router = useRouter()
const token = ref('')
const scanning = ref(false)
const showAdminLogin = ref(false)
const admin = ref({ username: '', password: '' })

const toggleCamera = () => (scanning.value = !scanning.value)

const handleManualLogin = () => {
    if (token.value.trim()) {
        router.push(`/respond/${token.value.trim()}`)
    } else {
        alert('Please enter a valid token')
    }
}

const onDetect = (detectedCodes: any[]) => {
    if (detectedCodes.length > 0) {
        const scannedToken = detectedCodes[0].rawValue
        router.push(`/respond/${scannedToken}`)
    }
}

const onError = (error: any) => {
    console.error('QR scan error:', error)
    alert('Unable to access camera. Please check permissions.')
}

import { mockAdmins } from '@/mock/users'

const handleAdminLogin = () => {
    const foundUser = mockAdmins.find(
        (u) =>
            u.username === admin.value.username.trim() &&
            u.password === admin.value.password.trim()
    )

    if (foundUser) {
        localStorage.setItem('adminAuth', JSON.stringify(foundUser))
        showAdminLogin.value = false
        router.push('/dashboard')
    } else {
        alert('Invalid username or password')
    }
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

.scale-enter-active,
.scale-leave-active {
    transition: all 0.25s ease;
}

.scale-enter-from {
    transform: scale(0.95);
    opacity: 0;
}

.scale-leave-to {
    transform: scale(0.95);
    opacity: 0;
}
</style>
