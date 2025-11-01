<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-50 to-blue-50 px-4">
    <div
      class="bg-white/80 backdrop-blur-md shadow-xl rounded-2xl p-8 max-w-lg w-full border border-gray-200 text-center"
    >
      <!-- Loading state -->
      <div v-if="loading" class="text-gray-500">Loading question...</div>

      <!-- Error state -->
      <div v-else-if="error" class="text-red-500">
        <p class="mb-4">{{ error }}</p>
        <button
          @click="goBack"
          class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
        >
          Back
        </button>
      </div>

      <!-- Question view -->
      <div v-else>
        <h2 class="text-2xl font-bold text-blue-600 mb-6">Your Question</h2>

        <div
          class="bg-blue-50 border border-blue-200 rounded-xl p-5 mb-6 text-left shadow-sm"
        >
          <p class="text-lg text-gray-800 mb-3 whitespace-pre-line">
            {{ question?.content }}
          </p>

          <p class="text-sm text-gray-500">
            <span v-if="question?.updated_at">
              Updated on {{ formatDate(question.updated_at) }}
            </span>
          </p>
        </div>

        <h3 class="text-lg font-semibold text-gray-700 mb-2">Your Answer</h3>

        <textarea
          v-model="answer"
          rows="5"
          placeholder="Write your answer here..."
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none mb-4"
        ></textarea>

        <button
          @click="handleSubmit"
          class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-60 disabled:cursor-not-allowed"
          :disabled="submitting || !answer.trim()"
        >
          {{ submitting ? "Submitting..." : "Submit Answer" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { getQuestionFromToken, createAnswer } from "@/api/answer"
import type { QuestionResponse } from "@/api/types"

const route = useRoute()
const router = useRouter()
const token = route.params.token as string

const question = ref<QuestionResponse | null>(null)
const answer = ref("")
const loading = ref(true)
const error = ref("")
const submitting = ref(false)
const success = ref(false)

/**
 * Fetch the question from API using the token
 */
const fetchQuestion = async () => {
  try {
    loading.value = true
    error.value = ""
    question.value = await getQuestionFromToken(token)
  } catch (err: any) {
    console.error("Error fetching question:", err)
    error.value = "Invalid or expired token."
  } finally {
    loading.value = false
  }
}

/**
 * Submit the answer
 */
const handleSubmit = async () => {
  if (!answer.value.trim()) return
  submitting.value = true
  success.value = false

  try {
    await createAnswer(token, answer.value.trim())
    router.push("/respond/success")
  } catch (err: any) {
    console.error("Error submitting answer:", err)
    alert(err?.response?.data?.detail || "Error submitting answer")
  } finally {
    submitting.value = false
  }
}

/**
 * Go back to the homepage
 */
const goBack = () => {
  router.push("/")
}

/**
 * Format date (optional utility)
 */
const formatDate = (iso: string) => {
  const date = new Date(iso)
  return date.toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  })
}

onMounted(fetchQuestion)
</script>
