<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/authStore"
import { LogOut, Brain, Eye, Trash, KeyRound, Plus } from "lucide-vue-next"
import ModalConfirm from "@/components/ModalConfirm.vue"
import ModalToken from "@/components/ModalToken.vue"
import { getAllQuestions, deleteQuestion, getQuestionInformation } from "@/api/question"
import { updateAnalysis } from "@/api/analysis"
import type { QuestionResponse, AnalyzeResponse } from "@/api/types"
import type { QuestionInformation } from "@/api/question"

const router = useRouter()
const auth = useAuthStore()

const questions = ref<QuestionResponse[]>([])
const questionInfo = ref<Record<number, QuestionInformation | null>>({})

const loading = ref(false)
const error = ref<string | null>(null)

// Modals
const deleteModalVisible = ref(false)
const analysisModalVisible = ref(false)
const tokenModalVisible = ref(false)
const selectedQuestionId = ref<number | null>(null)
const selectedToken = ref("")

// Loader overlay for AI analysis
const aiLoading = ref(false)

onMounted(async () => {
  if (!auth.isAuthenticated) router.push("/")
  await fetchQuestions()
})

/** Fetch all questions */
const fetchQuestions = async () => {
  loading.value = true
  error.value = null
  try {
    questions.value = await getAllQuestions()
    await fetchQuestionDetails()
  } catch (err) {
    console.error(err)
    error.value = "Failed to load questions."
  } finally {
    loading.value = false
  }
}

/** Fetch per-question info (answers, tokens, expiry) */
const fetchQuestionDetails = async () => {
  const infos = await Promise.all(
    questions.value.map((q) => getQuestionInformation(q.id).catch(() => null))
  )
  console.log(infos)
  
  infos.forEach((info, i) => {
    const id = questions.value[i].id
    questionInfo.value[id] = info
  })
}

/** Run AI Analysis */
const handleRunAnalysis = async (id: number) => {
  try {
    aiLoading.value = true
    const result: AnalyzeResponse = await updateAnalysis(id)
    setTimeout(() => {
      aiLoading.value = false
      router.push(`/dashboard/report/${id}`)
    }, 800)
  } catch (err) {
    console.error(err)
    aiLoading.value = false
    alert("Error running analysis.")
  }
}

/** Delete question */
const handleDeleteQuestion = async (id: number) => {
  try {
    await deleteQuestion(id)
    await fetchQuestions()
  } catch (err) {
    console.error(err)
    alert("Error deleting question.")
  }
}

/** View Report */
const handleViewReport = (id: number) => {
  router.push(`/dashboard/report/${id}`)
}

/** Show Token Modal */
const handleShowToken = (id: number) => {
  const tokens = questionInfo.value[id]?.tokens || []
  if (tokens.length > 0) {
    selectedToken.value =
      tokens.length === 1
        ? tokens[0].token_value
        : tokens.map((t) => t.token_value).join("\n")
    tokenModalVisible.value = true
  } else {
    alert("No tokens available for this question.")
  }
}

/** Logout */
const handleLogout = () => {
  auth.logout()
  router.push("/")
}

/** Add Question */
const handleAddQuestion = () => {
  router.push("/dashboard/addQuestion")
}

/** Opens modals */
const onClickDelete = (id: number) => {
  selectedQuestionId.value = id
  deleteModalVisible.value = true
}
const onClickRunAnalysis = (id: number) => {
  selectedQuestionId.value = id
  analysisModalVisible.value = true
}

/** Modals confirms */
const confirmDelete = async () => {
  if (selectedQuestionId.value === null) return
  await handleDeleteQuestion(selectedQuestionId.value)
}
const confirmRunAnalysis = async () => {
  if (selectedQuestionId.value === null) return
  await handleRunAnalysis(selectedQuestionId.value)
}

</script>

<template>
  <div class="min-h-screen bg-gray-50 relative overflow-hidden">
    <!-- Header -->
    <header
      class="flex flex-col sm:flex-row sm:items-center sm:justify-between bg-white p-4 shadow-sm gap-3 sm:gap-0"
    >
      <div>
        <h1 class="text-xl font-semibold text-gray-800">Questions Dashboard</h1>
        <p class="text-sm text-gray-500">Manage your questions and AI reports</p>
      </div>

      <div class="flex items-center gap-3">
        <!-- Add Question -->
        <button
          @click="handleAddQuestion"
          class="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl transition"
        >
          <Plus size="18" /> Add Question
        </button>

        <!-- Logout -->
        <button
          @click="handleLogout"
          class="flex items-center gap-2 bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-xl transition"
        >
          <LogOut size="18" /> Logout
        </button>
      </div>
    </header>

    <!-- Main -->
    <main class="p-6">
      <div v-if="loading" class="text-center text-gray-500 py-10">
        Loading questions...
      </div>
      <div v-else-if="error" class="text-center text-red-500 py-10">
        {{ error }}
      </div>

      <!-- Grid -->
      <div
        v-else
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"
      >
        <div
          v-for="q in questions"
          :key="q.id"
          class="bg-white rounded-2xl shadow p-5 flex flex-col justify-between hover:shadow-md transition"
        >
          <!-- Content + Info -->
          <div>
            <h2
              class="text-lg font-semibold text-gray-800 mb-2 break-words truncate-multiline"
            >
              {{ q.content }}
            </h2>

            <!-- Detailed infos -->
            <div v-if="questionInfo[q.id]" class="text-sm text-gray-600 space-y-1">
              <p>
                <strong>Answers:</strong>
                {{ questionInfo[q.id]?.answers_count ?? 0 }}
              </p>

              <p v-if="questionInfo[q.id]?.tokens?.length">
                <strong>Expires:</strong>
                {{
                  questionInfo[q.id]?.tokens[0]?.expire_at
                    ? new Date(
                        questionInfo[q.id]?.tokens[0]?.expire_at
                      ).toLocaleString()
                    : "Never"
                }}
              </p>
            </div>

            <p v-else class="text-gray-400 text-sm italic">
              Loading details...
            </p>
          </div>

          <!-- Buttons -->
          <div class="flex justify-end gap-2 mt-4">
            <!-- Token -->
            <button
              @click="handleShowToken(q.id)"
              class="p-2 rounded-lg bg-yellow-50 hover:bg-yellow-100 text-yellow-600 transition"
              title="Show Token"
            >
              <KeyRound size="18" />
            </button>

            <!-- Run AI -->
            <button
              @click="onClickRunAnalysis(q.id)"
              :disabled="(questionInfo[q.id]?.answers_count || 0) === 0"
              :class="[ 
                'p-2 rounded-lg transition',
                (questionInfo[q.id]?.answers_count || 0) === 0
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-purple-50 hover:bg-purple-100 text-purple-600',
              ]"
              title="Run AI Report"
            >
              <Brain size="18" />
            </button>

            <!-- View Report -->
            <button
              @click="handleViewReport(q.id)"
              :disabled="questionInfo[q.id]?.report_id == null"
              :class="[
                'p-2 rounded-lg transition',
                !questionInfo[q.id]?.report_id
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-blue-50 hover:bg-blue-100 text-blue-600',
              ]"
              title="View Report"
            >
              <Eye size="18" />
            </button>

            <!-- Delete -->
            <button
              @click="onClickDelete(q.id)"
              class="p-2 rounded-lg bg-red-50 hover:bg-red-100 text-red-600 transition"
              title="Delete Question"
            >
              <Trash size="18" />
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Modals -->
    <ModalConfirm
      v-model="deleteModalVisible"
      title="Delete Question"
      message="Are you sure you want to delete this question?"
      @confirmed="confirmDelete"
    />

    <ModalConfirm
      v-model="analysisModalVisible"
      title="Run AI Analysis"
      message="Run AI analysis for this question?"
      @confirmed="confirmRunAnalysis"
    />

    <ModalToken v-model="tokenModalVisible" :token="selectedToken" />

    <!-- Loader Overlay -->
    <transition name="fade">
      <div
        v-if="aiLoading"
        class="fixed inset-0 flex flex-col items-center justify-center bg-white/80 backdrop-blur-sm z-50"
      >
        <div
          class="w-12 h-12 border-4 border-blue-400 border-t-transparent rounded-full animate-spin mb-4"
        ></div>
        <p class="text-gray-600 text-lg font-medium">
          Running AI Analysis...
        </p>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.truncate-multiline {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  word-break: break-word;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.space-y-1 > * + * {
  margin-top: 0.25rem;
}
</style>
