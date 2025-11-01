<template>
    <div class="p-6">

        <div class="flex justify-between items-center mb-6">
            <div>
                <h1 class="text-2xl font-bold text-gray-800">Admin Dashboard</h1>
                <p class="text-gray-500 text-sm">
                    Welcome back, <span class="font-semibold">{{ adminUser?.name }}</span> ({{ adminUser?.role }})
                </p>
            </div>
            <button @click="handleLogout"
                class="text-sm px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition">
                Logout
            </button>
        </div>

        <Nav />
        <h2 class="text-2xl font-bold mt-6 mb-4">Open Topics</h2>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <TopicCard v-for="topic in store.topics" :key="topic.id" :topic="topic"
                @remove="store.removeTopic(topic.id)" />
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Nav from '@/components/Nav.vue';
import TopicCard from '@/components/TopicCard.vue';
import { useTopicsStore } from '@/store/topics';

const store = useTopicsStore();
const router = useRouter();
const adminUser = ref<{ name: string; role: string } | null>(null);

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
</script>