<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { getTeam, updateTeam } from "@/api/team"
import { listUsers, createUser } from "@/api/user"

const route = useRoute()
const router = useRouter()
const teamId = Number(route.params.id)

// --- STATE ---
const team = ref<any>(null)
const users = ref<any[]>([])
const selectedUsers = ref<number[]>([])
const newTeamName = ref("")
const loading = ref(true)
const saving = ref(false)
const message = ref<string | null>(null)
const error = ref<string | null>(null)

// --- USER CREATION ---
const newUser = ref({ name: "", lastname: "", email: "" })
const userError = ref<string | null>(null)
const creatingUser = ref(false)

// --- FETCH TEAM DATA ---
const fetchTeam = async () => {
  loading.value = true
  error.value = null
  try {
    const data = await getTeam(teamId)

    if (!data || !data.id) {
      throw new Error("Invalid or missing team data")
    }

    team.value = data
    selectedUsers.value = data.users_ids || []
    newTeamName.value = data.name || ""
    console.log("Team fetched:", data)
  } catch (err) {
    console.error("Failed to fetch team:", err)
    error.value = "Error loading team data."
  } finally {
    loading.value = false
  }
}

// --- FETCH USERS DATA ---
const fetchUsers = async () => {
  try {
    const data = await listUsers()

    if (Array.isArray(data)) {
      users.value = data.filter(u => u && u.id && u.name)
      console.log("✅ Users fetched:", users.value)
    } else {
      console.warn("⚠️ Unexpected /user/ response format:", data)
      users.value = []
    }
  } catch (err) {
    console.error("❌ Failed to fetch users:", err)
    error.value = "Error loading users."
    users.value = []
  }
}

// --- CREATE USER ---
const handleCreateUser = async () => {
  userError.value = null

  if (!newUser.value.name.trim()) {
    userError.value = "Name is required."
    return
  }
  if (!newUser.value.lastname.trim()) {
    userError.value = "Last name is required."
    return
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(newUser.value.email)) {
    userError.value = "Invalid email address."
    return
  }

  try {
    creatingUser.value = true
    await createUser({ ...newUser.value, team_id: teamId })
    newUser.value = { name: "", lastname: "", email: "" }
    await fetchUsers()
    await fetchTeam()
    message.value = "User created successfully!"
  } catch (err) {
    console.error("❌ Error creating user:", err)
    userError.value = "Error while creating user."
  } finally {
    creatingUser.value = false
  }
}

// --- SAVE TEAM NAME + USERS ---
const handleSaveAll = async () => {
  saving.value = true
  message.value = null
  try {
    await updateTeam(teamId, {
      name: newTeamName.value.trim(),
      users_ids: selectedUsers.value,
    })
    message.value = "Team updated successfully!"
    await fetchTeam()
  } catch (err) {
    console.error("Failed to update team:", err)
    message.value = "Error while updating team."
  } finally {
    saving.value = false
  }
}

// --- ON MOUNT ---
onMounted(async () => {
  await fetchTeam()
  await fetchUsers()
})
</script>

<template>
  <div
      class="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-50 to-blue-50 px-4"
  >
    <div
        class="bg-white/80 backdrop-blur-md shadow-xl rounded-2xl p-8 max-w-2xl w-full border border-gray-200"
    >
      <!-- HEADER -->
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-3xl font-bold text-blue-600">Manage Team</h2>
        <button
            @click="router.push('/dashboard/teams')"
            class="text-blue-600 hover:text-blue-800 transition font-medium"
        >
          Back
        </button>
      </div>

      <!-- LOADING / ERROR STATES -->
      <div v-if="loading" class="text-gray-600 text-center">Loading...</div>
      <div v-else-if="error" class="text-red-600 text-center">{{ error }}</div>

      <!-- MAIN CONTENT -->
      <div v-else-if="team" class="space-y-6">
        <!-- TEAM NAME -->
        <div>
          <label class="block text-left font-medium text-gray-700 mb-2">
            Team Name
          </label>
          <input
              v-model="newTeamName"
              type="text"
              placeholder="Enter team name..."
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
          />
        </div>

        <!-- ADD USER -->
        <div>
          <h3 class="text-xl font-semibold text-blue-600 mb-2">
            Add a New User
          </h3>

          <div class="space-y-2">
            <input
                v-model="newUser.name"
                type="text"
                placeholder="First name"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
            <input
                v-model="newUser.lastname"
                type="text"
                placeholder="Last name"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
            <input
                v-model="newUser.email"
                type="email"
                placeholder="Email"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />

            <button
                @click="handleCreateUser"
                :disabled="creatingUser"
                class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
            >
              {{ creatingUser ? "Creating..." : "Create User" }}
            </button>

            <p v-if="userError" class="text-red-600 text-sm text-center">
              {{ userError }}
            </p>
          </div>
        </div>

        <!-- ASSIGN USERS -->
        <div>
          <h3 class="text-xl font-semibold text-blue-600 mb-2">
            Assign Users to Team
          </h3>

          <div
              class="max-h-48 overflow-y-auto border border-gray-200 rounded-lg bg-white shadow-inner"
          >
            <label
                v-for="user in users"
                :key="user.id"
                class="flex items-center gap-2 px-3 py-2 hover:bg-blue-50 cursor-pointer"
            >
              <input
                  type="checkbox"
                  v-model="selectedUsers"
                  :value="user.id"
                  class="accent-blue-600"
              />
              <span class="text-gray-700">
                {{ user.name }} {{ user.lastname }}
                <span class="text-gray-400 text-sm">({{ user.email }})</span>
              </span>
            </label>

            <p
                v-if="!users.length"
                class="text-gray-400 text-sm text-center py-3"
            >
              No users available — create one above.
            </p>
          </div>
        </div>

        <!-- SAVE BUTTON -->
        <button
            @click="handleSaveAll"
            :disabled="saving"
            class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
        >
          {{ saving ? "Saving..." : "Save All Changes" }}
        </button>

        <p v-if="message" class="text-green-600 text-center mt-4">
          {{ message }}
        </p>
      </div>

      <!-- EMPTY STATE -->
      <div v-else class="text-gray-500 text-center py-6">
        Team not found.
      </div>
    </div>
  </div>
</template>

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
