<template>
    <div class="max-w-3xl mx-auto p-8">
        <h1 class="text-2xl font-bold mb-4">{{ topic.title }}</h1>
        <p class="text-gray-700 mb-6">{{ topic.description }}</p>

        <h2 class="text-xl font-semibold mb-2">Share Your Opinion</h2>
        <OpinionForm :topic-id="topic.id" />

        <h2 class="text-xl font-semibold mt-8 mb-2">Community Insights</h2>
        <ul class="space-y-3">
            <li v-for="op in topic.opinions" :key="op.id" class="p-3 bg-gray-100 rounded-xl">
                {{ op.text }}
            </li>
        </ul>

        <ConsensusSummary :topic-id="topic.id" class="mt-8" />
    </div>
</template>

<script lang="ts" setup>
import { useRoute } from 'vue-router';
import { useTopicsStore } from '@/store/topics';
import OpinionForm from '@/components/OpinionForm.vue';
import ConsensusSummary from '@/components/ConsensusSummary.vue';

const route = useRoute();
const store = useTopicsStore();
const topic = store.getTopicById(Number(route.params.id));
</script>
