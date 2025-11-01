<template>
    <nav class="bg-white shadow-md rounded-xl px-6 py-3 flex justify-between items-center relative z-10">
        <h1 class="text-xl font-bold text-blue-600">inSintesi TeamLead</h1>
        <ul class="flex space-x-4 text-gray-600">
            <li><router-link to="/" class="hover:text-blue-600">Dashboard</router-link></li>
            <li @click="openModal" class="hover:text-blue-600">Add topic</li>
            <AddTopic v-if="showModal" @close="closeModal" />
        </ul>
    </nav>
</template>


<script lang="ts" setup>
import { ref } from 'vue';
import AddTopic from './AddTopic.vue';

const showModal = ref(false);

const openModal = () => (showModal.value = true);
const closeModal = () => (showModal.value = false);
</script>