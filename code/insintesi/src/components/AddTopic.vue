<template>
    <!-- Overlay -->
    <div class="fixed inset-0 bg-black/40 backdrop-blur-sm flex justify-center items-center z-50" @click.self="close">
        <!-- Modal -->
        <div class="bg-white rounded-xl shadow-xl w-full max-w-md p-6 relative animate-fadeIn" @click.stop>
            <!-- Close Button (optional top-right X) -->
            <button @click="close" class="absolute top-3 right-3 text-gray-400 hover:text-gray-600 text-xl"
                aria-label="Close">
                ×
            </button>

            <h2 class="text-lg font-semibold mb-4">Add a new topic</h2>

            <form @submit.prevent="handleSubmit" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Title</label>
                    <input v-model="title" type="text" required
                        class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500" />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
                    <textarea v-model="description" rows="3" required
                        class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500"></textarea>
                </div>

                <div class="flex justify-end space-x-3 pt-4">
                    <button type="button" @click="close"
                        class="px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300 transition">
                        Cancel
                    </button>

                    <button type="submit"
                        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
                        Add Topic
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useTopicsStore } from '@/store/topics';

const emit = defineEmits(['close']);
const store = useTopicsStore();

const title = ref('');
const description = ref('');

// Close modal handler
const close = () => emit('close');

// Add topic + close modal
const handleSubmit = () => {
    store.addTopic(title.value, description.value);
    close();
    title.value = '';
    description.value = '';
};

// Prevent background scrolling while modal open
onMounted(() => {
    document.body.style.overflow = 'hidden';
});
onUnmounted(() => {
    document.body.style.overflow = '';
});
</script>

<style scoped>
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: scale(0.95);
    }

    to {
        opacity: 1;
        transform: scale(1);
    }
}

.animate-fadeIn {
    animation: fadeIn 0.2s ease-out;
}
</style>
