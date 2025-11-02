<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { listTeams, createTeam, deleteTeam, type Team } from '@/api/team'
import { Plus, Trash } from 'lucide-vue-next'

const teams = ref<Team[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const showAddModal = ref(false)
const newTeamName = ref('')

/**
 * Load all teams when component mounts.
 */
onMounted(async () => {
  await fetchTeams()
})

/**
 * Fetch the list of teams.
 */
const fetchTeams = async () => {
  loading.value = true
  error.value = null
  try {
    teams.value = await listTeams()
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load teams.'
  } finally {
    loading.value = false
  }
}

/**
 * Create a new team.
 */
const handleAddTeam = async () => {
  if (!newTeamName.value.trim()) return
  try {
    await createTeam({ name: newTeamName.value.trim() })
    newTeamName.value = ''
    showAddModal.value = false
    await fetchTeams()
  } catch (err) {
    console.error('Failed to create team:', err)
  }
}

/**
 * Delete a team.
 */
const handleDeleteTeam = async (id: number) => {
  if (!confirm('Are you sure you want to delete this team?')) return
  try {
    await deleteTeam(id)
    await fetchTeams()
  } catch (err) {
    console.error('Failed to delete team:', err)
  }
}
</script>

<template>
  <div class="p-6">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-semibold text-gray-800">My Teams</h1>
      <button
          @click="showAddModal = true"
          class="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition"
      >
        <Plus size="18" /> Add Team
      </button>
    </div>

    <!-- Loading and Error States -->
    <div v-if="loading" class="text-gray-500">Loading teams...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>

    <!-- Teams Grid -->
    <div
        v-else
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"
    >
      <div
          v-for="team in teams"
          :key="team.id"
          @click="$router.push({ name: 'team-detail', params: { id: team.id } })"
          class="bg-white shadow rounded-2xl p-6 flex justify-between items-center hover:shadow-md transition border border-gray-100 cursor-pointer"
      >
        <span class="text-lg font-semibold text-gray-800">{{ team.name }}</span>

        <button
            @click.stop="handleDeleteTeam(team.id)"
            class="p-2 rounded-lg bg-red-50 hover:bg-red-100 text-red-600 transition"
        >
          <Trash size="18" />
        </button>
      </div>

    </div>

    <!-- Add Team Modal -->
    <div
        v-if="showAddModal"
        @click.self="showAddModal = false"
        class="fixed inset-0 bg-black/50 flex justify-center items-center z-50 transition"
    >
      <div class="bg-white p-6 rounded-2xl shadow-lg w-80">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">Add a new team</h3>

        <input
            v-model="newTeamName"
            type="text"
            placeholder="Enter team name..."
            class="w-full border border-gray-300 rounded-lg p-2 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <div class="flex justify-end gap-2">
          <button
              @click="showAddModal = false"
              class="px-4 py-2 rounded-lg border text-gray-600 hover:bg-gray-100 transition"
          >
            Cancel
          </button>
          <button
              @click="handleAddTeam"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            Enter
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
