<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useTopicStore } from '@/stores/topics';
import { Plus, LogOut, Eye, Trash } from 'lucide-vue-next';

const router = useRouter();
const topicStore = useTopicStore();
const adminUser = ref<{ name: string; role: string } | null>(null);
const showAddModal = ref(false);
const newTopicTitle = ref('');

onMounted(() => {
    const stored = localStorage.getItem('adminAuth');
    if (stored) {
        adminUser.value = JSON.parse(stored);
    } else {
        router.push('/');
    }
});

const handleLogout = () => {
    localStorage.removeItem('adminAuth');
    router.push('/');
};

const handleAddTopic = () => {
    if (newTopicTitle.value.trim()) {
        topicStore.addTopic(newTopicTitle.value.trim());
        newTopicTitle.value = '';
        showAddModal.value = false;
    }
};

const handleDeleteTopic = (id: number) => {
    if (confirm('Are you sure you want to delete this topic?')) {
        topicStore.removeTopic(id);
    }
};

const handleViewTopic = (id: number) => {
    router.push(`/topic/${id}`);
};
</script>

<template>
    <div>
        <!-- Header -->
        <header class="flex items-center justify-between bg-white m-12 p-4 shadow-sm">
            <div>
                <h1 class="text-xl font-semibold text-gray-800">inSintesi dashboard</h1>
                <p class="text-sm text-gray-500">
                    Logged in as
                    <span class="font-medium text-gray-700">{{ adminUser?.name }}</span>
                    — {{ adminUser?.role }}
                </p>
            </div>

            <div class="flex items-center gap-3">
                <button @click="showAddModal = true"
                    class="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl transition">
                    <Plus size="18" /> Add topic
                </button>

                <button @click="handleLogout"
                    class="flex items-center gap-2 bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-xl transition">
                    <LogOut size="18" /> Logout
                </button>
            </div>
        </header>

        <!-- Topics List -->
        <main class="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="topic in topicStore.topics" :key="topic.id"
                class="bg-white rounded-2xl shadow p-4 flex flex-col justify-between hover:shadow-md transition">
                <div>
                    <h2 class="text-lg font-semibold text-gray-800 mb-2">{{ topic.title }}</h2>
                    <p class="text-sm text-gray-500">
                        Responses: {{ topic.responses?.length || 0 }}
                    </p>
                </div>
                <div class="flex justify-end gap-2 mt-4">
                    <button @click="handleViewTopic(topic.id)"
                        class="p-2 rounded-lg bg-blue-50 hover:bg-blue-100 text-blue-600 transition">
                        <Eye size="18" />
                    </button>
                    <button @click="handleDeleteTopic(topic.id)"
                        class="p-2 rounded-lg bg-red-50 hover:bg-red-100 text-red-600 transition">
                        <Trash size="18" />
                    </button>
                </div>
            </div>
        </main>

        <!-- Add Topic Modal -->
        <div v-if="showAddModal" @click.self="showAddModal = false"
            class="fixed inset-0 bg-black/50 flex justify-center items-center z-50 transition">
            <div class="bg-white p-6 rounded-2xl shadow-lg w-80">
                <h3 class="text-lg font-semibold text-gray-800 mb-4">Add a new topic</h3>
                <input v-model="newTopicTitle" type="text" placeholder="Enter topic question..."
                    class="w-full border border-gray-300 rounded-lg p-2 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                <div class="flex justify-end gap-2">
                    <button @click="showAddModal = false"
                        class="px-4 py-2 rounded-lg border text-gray-600 hover:bg-gray-100 transition">
                        Cancel
                    </button>
                    <button @click="handleAddTopic"
                        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
                        Enter
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
