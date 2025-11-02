<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-50 to-blue-50 px-4"
  >
    <div
      class="bg-white/80 backdrop-blur-md shadow-xl rounded-2xl p-8 max-w-2xl w-full border border-gray-200"
    >
      <h2 class="text-3xl font-bold text-blue-600 mb-6 text-center">
        Create a New Question
      </h2>

      <!-- FORM -->
      <form @submit.prevent="handleSubmit" class="space-y-5">
        <!-- Question -->
        <div>
          <label class="block text-left font-medium text-gray-700 mb-2">Question</label>
          <textarea
            v-model="form.content"
            rows="4"
            placeholder="Write your question..."
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            required
          ></textarea>
        </div>

        <!-- Token Type -->
        <div>
          <label class="block text-left font-medium text-gray-700 mb-2">Token Type</label>
          <select
            v-model="form.token_type"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
          >
            <option value="universal">Universal (valid for anyone)</option>
            <option value="individual">Restricted to Teams</option>
          </select>
        </div>

        <!-- Teams (only if token_type === team) -->
        <div v-if="form.token_type === 'individual'">
          <label class="block text-left font-medium text-gray-700 mb-2">Select Teams</label>

          <!-- Search bar -->
          <input
            v-model="teamSearch"
            type="text"
            placeholder="Search team..."
            class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
          />

          <!-- Filtered list -->
          <div class="max-h-40 overflow-y-auto border border-gray-200 rounded-lg bg-white shadow-sm">
          <div
            v-for="team in filteredTeams"
            :key="team.id"
            class="flex items-center px-3 py-2 hover:bg-blue-50 cursor-pointer"
            >
            <input
              type="checkbox"
              class="mr-2 accent-blue-600"
              :checked="form.teams_ids.includes(Number(team.id))"
              @change="onToggleTeam($event, Number(team.id))"
            />
            <span class="text-gray-700">Team #{{ team.id }} {{ team.name }}</span>
          </div>


          <p
            v-if="filteredTeams.length === 0"
            class="text-gray-400 text-sm text-center py-2"
          >
            No teams found
          </p>
        </div>
      </div>

        <!-- Expiration Date -->
        <div>
          <label class="block text-left font-medium text-gray-700 mb-2">
            Expiration
          </label>

          <div class="flex items-center space-x-2">
            <input
              v-model="noExpiry"
              type="checkbox"
              id="noExpiry"
              class="w-4 h-4 accent-blue-600"
            />
            <label for="noExpiry" class="text-gray-700 text-sm">
              Never expire
            </label>
          </div>

          <input
            v-if="!noExpiry"
            v-model="expiryDate"
            type="datetime-local"
            class="mt-2 w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
          />
        </div>

        <!-- Submit -->
        <button
          type="submit"
          class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
          :disabled="loading"
        >
          {{ loading ? "Creating..." : "Create Question" }}
        </button>
      </form>

      <!-- Error -->
      <div v-if="errorMessage" class="mt-6 text-red-500 text-center">
        {{ errorMessage }}
      </div>
    </div>

    <!-- MODAL for Universal Token -->
    <transition name="fade">
      <div
        v-if="showTokenModal"
        class="fixed inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm z-50"
      >
        <div
          class="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-lg text-center border border-gray-100 relative"
        >
          <h3 class="text-2xl font-semibold text-blue-600 mb-4">Your Access Token</h3>
          <p class="text-gray-700 mb-6">
            Share this token with participants. They can use it to respond.
          </p>

          <div
            class="bg-blue-50 border border-blue-200 text-blue-700 font-mono text-xl rounded-lg px-6 py-4 mb-4 select-all break-all"
          >
            {{ generatedToken }}
          </div>

          <button
            @click="copyToken"
            class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition mb-3"
          >
            Copy to Clipboard
          </button>

          <button
            @click="closeModal"
            class="w-full border border-gray-300 text-gray-600 py-2 rounded-lg hover:bg-gray-100 transition"
          >
            Close
          </button>
        </div>
      </div>
    </transition>

    <!-- MODAL for Team Confirmation -->
    <transition name="fade">
      <div
        v-if="showTeamModal"
        class="fixed inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm z-50"
      >
        <div
          class="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-lg text-center border border-gray-100 relative"
        >
          <h3 class="text-2xl font-semibold text-blue-600 mb-4">✅ Question Created</h3>
          <p class="text-gray-700 mb-6">
            Emails with tokens have been successfully sent to all selected team members.
          </p>

          <button
            @click="closeTeamModal"
            class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
          >
            Close
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted, reactive } from "vue"
import { useAuthStore } from "@/stores/authStore"
import { createQuestion } from "@/api/question"
import { listTeams } from "@/api/team"
import type { QuestionCreate } from "@/api/types"
import type { Team } from "@/api/types"

const auth = useAuthStore()

const form = reactive<QuestionCreate>({
  content: "",
  team_lead_id: 0,
  token_type: "universal",
  teams_ids: [],
  expires_at: null,
})

// State
const loading = ref(false)
const errorMessage = ref("")

// Token modal
const showTokenModal = ref(false)
const generatedToken = ref("")

// Team modal
const showTeamModal = ref(false)

// Team selection
const teams = ref<Team[]>([])
const teamSearch = ref("")
const filteredTeams = computed(() => {
  const search = teamSearch.value.toLowerCase()
  return teams.value.filter((t: any) => String(t.id).toLowerCase().includes(search))
})

// Expiration
const noExpiry = ref(false)
const expiryDate = ref("")

// Load available teams
const fetchTeams = async () => {
  try {
    teams.value = await listTeams()
  } catch (err) {
    console.error("Error loading teams:", err)
  }
}

// Submit form
const handleSubmit = async () => {
  errorMessage.value = ""
  generatedToken.value = ""
  showTokenModal.value = false
  showTeamModal.value = false

  try {
    if (!auth.isAuthenticated) throw new Error("You must be logged in.")
    form.team_lead_id = 1 // TODO: Replace with real ID

    if (form.token_type === "universal") {
      form.teams_ids = []
    }

    // Expiration
    form.expires_at = noExpiry.value
      ? null
      : expiryDate.value
      ? new Date(expiryDate.value).toISOString()
      : null

      console.log(form.expires_at)

    loading.value = true
    const payload = JSON.parse(JSON.stringify(form))
    const res = await createQuestion(payload)

    if (form.token_type === "universal" && res.tokens.length > 0) {
      if (res.tokens[0] != undefined) {
        generatedToken.value = res.tokens[0]
      }
      showTokenModal.value = true
    } else {
      showTeamModal.value = true
    }

    // Reset form
    form.content = ""
    form.teams_ids = []
    expiryDate.value = ""
    noExpiry.value = false
  } catch (err: any) {
    console.error("Error creating question:", err)
    errorMessage.value =
      err?.response?.data?.detail || "Unable to create question."
  } finally {
    loading.value = false
  }
}

// Copy token to clipboard
const copyToken = async () => {
  await navigator.clipboard.writeText(generatedToken.value)
  showTokenModal.value = false
}

// Close modals
const closeModal = () => (showTokenModal.value = false)
const closeTeamModal = () => (showTeamModal.value = false)

const onToggleTeam = (e: Event, id: number) => {
  const checked = (e.target as HTMLInputElement).checked
  if (checked) {
    if (!form.teams_ids.includes(id)) form.teams_ids.push(id)
  } else {
    form.teams_ids.splice(form.teams_ids.indexOf(id), 1)
    console.log(form.teams_ids)
  }
}


onMounted(fetchTeams)
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
