<template>
    <div class="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-6">
        <div class="bg-white shadow-md rounded-xl p-8 w-full max-w-lg">
            <h1 class="text-2xl font-bold mb-2 text-gray-800 text-center">Your Response</h1>
            <p class="text-gray-500 text-sm text-center mb-6">
                Token: <span class="font-mono text-blue-600">{{ token }}</span>
            </p>

            <p class="text-gray-700 mb-4">
                {{ topicQuestion || "Please answer the following question:" }}
            </p>

            <textarea v-model="answer" placeholder="Write your thoughts here..." rows="6"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 mb-4"></textarea>

            <div class="flex justify-end">
                <button @click="submitAnswer"
                    class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
                    :disabled="loading">
                    {{ loading ? "Submitting..." : "Submit" }}
                </button>
            </div>

            <div v-if="submitted"
                class="mt-6 p-4 bg-green-50 border border-green-200 text-green-800 rounded-lg text-center">
                ✅ Thank you for your response!
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

// Simulate topic lookup (in production, you’d fetch this via API)
import { mockTopics } from '@/mock/topics';

const route = useRoute();
const token = route.params.token as string;

const topicQuestion = ref<string | null>(null);
const answer = ref('');
const loading = ref(false);
const submitted = ref(false);

onMounted(() => {
    // Example: token contains topic ID
    const topic = mockTopics.find(t => String(t.id) === token);
    if (topic) {
        topicQuestion.value = topic.title;
    } else {
        topicQuestion.value = 'What are your thoughts on this topic?';
    }
});

const submitAnswer = async () => {
    if (!answer.value.trim()) {
        alert('Please write a response before submitting.');
        return;
    }

    loading.value = true;
    // Simulate an API call
    await new Promise(res => setTimeout(res, 1000));

    loading.value = false;
    submitted.value = true;
    answer.value = '';
};
</script>
