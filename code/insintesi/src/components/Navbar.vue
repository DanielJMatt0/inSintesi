<template>
  <nav
    class="flex items-center justify-between w-full px-4 py-3 bg-white border-b border-gray-200 shadow-sm"
  >
    <div class="flex items-center gap-3">
      <button
        @click="goBack"
        class="flex items-center gap-1 text-gray-600 hover:text-gray-900 transition"
        title="Go back"
      >
        <ArrowLeft class="w-5 h-5" />
      </button>

      <h1 class="text-lg font-semibold text-gray-800">
        {{ currentTitle }}
      </h1>
    </div>

    <div class="flex items-center gap-3">
      <template v-if="isDashboard">
        <button
          @click="goToAddQuestion"
          class="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-3 py-1.5 rounded-lg transition text-sm"
        >
          <Plus size="16" /> Add Question
        </button>

        <button
          @click="goToTeams"
          class="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white px-3 py-1.5 rounded-lg transition text-sm"
        >
          <Users size="16" /> Teams
        </button>
      </template>

      <button
        @click="logout"
        class="flex items-center gap-1 text-red-600 hover:text-red-700 transition font-medium"
        title="Logout"
      >
        <LogOut class="w-5 h-5" />
        <span class="hidden sm:inline">Logout</span>
      </button>
    </div>
  </nav>
</template>


<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { computed } from 'vue'
import { ArrowLeft, LogOut, Plus, Users } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const currentTitle = computed(() => route.meta.title || (route.name as string) || 'Dashboard')

const isDashboard = computed(() => route.path.startsWith('/dashboard'))

const goBack = () => {
  if (window.history.length > 1) router.back()
  else router.push('/')
}

const goToAddQuestion = () => {
  router.push('/dashboard/addQuestion')
}

const goToTeams = () => {
  router.push('/dashboard/teams')
}

const logout = () => {
  auth.logout()
  router.push('/')
}
</script>

<style scoped>
nav {
  backdrop-filter: blur(8px);
  background-color: rgba(255, 255, 255, 0.9);
}
</style>
