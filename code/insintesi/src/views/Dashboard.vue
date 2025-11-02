<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore.ts';
import { Plus, LogOut, Eye, Trash } from 'lucide-vue-next';
import {
    getAllQuestions,
    createQuestion,
    deleteQuestion,
} from '@/api/question';
import type { QuestionResponse, QuestionCreate } from '@/api/types';

const router = useRouter();
const auth = useAuthStore();
const adminUser = ref<{ name: string; role: string } | null>(null);
const questions = ref<QuestionResponse[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

const showAddModal = ref(false);
const newQuestionText = ref('');

onMounted(async () => {
    if (!auth.isAuthenticated) router.push("/");
    await fetchQuestions();
});

/**
 * Fetch all questions
 */
const fetchQuestions = async () => {
    loading.value = true;
    error.value = null;
    try {
        questions.value = await getAllQuestions();
    } catch (err: any) {
        error.value = 'Failed to load questions.';
        console.error(err);
    } finally {
        loading.value = false;
    }
};

/**
 * Add a new question
 */
const handleAddQuestion = async () => {
    if (!newQuestionText.value.trim()) return;

    const payload: QuestionCreate = {
        text: newQuestionText.value.trim(),
    };

    try {
        await createQuestion(payload);
        newQuestionText.value = '';
        showAddModal.value = false;
        await fetchQuestions();
    } catch (err) {
        alert('Error creating question.');
        console.error(err);
    }
};

/**
 * Delete question
 */
const handleDeleteQuestion = async (id: number) => {
    if (!confirm('Are you sure you want to delete this question?')) return;
    try {
        await deleteQuestion(id);
        await fetchQuestions();
    } catch (err) {
        alert('Error deleting question.');
        console.error(err);
    }
};

/**
 * View question
 */
const handleViewQuestion = (id: number) => {
    router.push(`/topic/${id}`);
};

/**
 * Logout
 */
const handleLogout = () => {
    auth.logout();
    router.push("/");
};
</script>

<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Header -->
        <header class="flex items-center justify-between bg-white p-4 shadow-sm">
            <div>
                <h1 class="text-xl font-semibold text-gray-800">Admin Dashboard</h1>
                <p class="text-sm text-gray-500">
                    Logged in as
                    <span class="font-medium text-gray-700">{{ adminUser?.name }}</span>
                    — {{ adminUser?.role }}
                </p>
            </div>

            <div class="flex items-center gap-3">
                <button @click="showAddModal = true"
                    class="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl transition">
                    <Plus size="18" /> Add Question
                </button>

                <button @click="handleLogout"
                    class="flex items-center gap-2 bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-xl transition">
                    <LogOut size="18" /> Logout
                </button>
            </div>
        </header>

        <!-- Main Content -->
        <main class="p-6">
            <!-- Loading & Error States -->
            <div v-if="loading" class="text-center text-gray-500 py-10">
                Loading questions...
            </div>
            <div v-else-if="error" class="text-center text-red-500 py-10">
                {{ error }}
            </div>

            <!-- Questions Grid -->
            <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div v-for="q in questions" :key="q.id"
                    class="bg-white rounded-2xl shadow p-4 flex flex-col justify-between hover:shadow-md transition">
                    <div>
                        <h2 class="text-lg font-semibold text-gray-800 mb-2 break-words truncate-multiline">
                            {{ q.text }}
                        </h2>
                        <p class="text-sm text-gray-500">
                            Participants: {{ q.participants_count || 0 }}
                        </p>
                    </div>

                    <div class="flex justify-end gap-2 mt-4">
                        <button @click="handleViewQuestion(q.id)"
                            class="p-2 rounded-lg bg-blue-50 hover:bg-blue-100 text-blue-600 transition">
                            <Eye size="18" />
                        </button>
                        <button @click="handleDeleteQuestion(q.id)"
                            class="p-2 rounded-lg bg-red-50 hover:bg-red-100 text-red-600 transition">
                            <Trash size="18" />
                        </button>
                    </div>
                </div>
            </div>
        </main>

        <!-- Add Question Modal -->
        <transition name="fade-scale">
            <div v-if="showAddModal" @click.self="showAddModal = false"
                class="fixed inset-0 bg-black/50 flex justify-center items-center z-50 transition">
                <div class="bg-white p-8 rounded-2xl shadow-lg w-[90%] max-w-lg animate-pop">
                    <h3 class="text-xl font-semibold text-gray-800 mb-4">
                        Add New Question
                    </h3>
                    <textarea v-model="newQuestionText" placeholder="Enter the question text..." rows="5"
                        class="w-full border border-gray-300 rounded-lg p-3 mb-4 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
                    <div class="flex justify-end gap-2">
                        <button @click="showAddModal = false"
                            class="px-4 py-2 rounded-lg border text-gray-600 hover:bg-gray-100 transition">
                            Cancel
                        </button>
                        <button @click="handleAddQuestion"
                            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
                            Add
                        </button>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<style scoped>
.fade-scale-enter-active,
.fade-scale-leave-active {
    transition: all 0.25s ease;
}

.fade-scale-enter-from,
.fade-scale-leave-to {
    opacity: 0;
    transform: scale(0.95);
}

@keyframes pop {
    0% {
        transform: scale(0.95);
        opacity: 0;
    }

    100% {
        transform: scale(1);
        opacity: 1;
    }
}

.animate-pop {
    animation: pop 0.25s ease;
}

.truncate-multiline {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    word-break: break-word;
}
</style>
