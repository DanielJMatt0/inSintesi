import { defineStore } from 'pinia';
import { ref } from 'vue';
import { mockTopics } from '@/mock/topics';

export const useTopicsStore = defineStore('topics', () => {
    const topics = ref([...mockTopics]);

    function addTopic(title: string, description: string) {
        const newTopic = {
            id: Date.now(),
            title,
            description,
            responses: 0,
        };
        topics.value.push(newTopic);
    }

    function removeTopic(id: number) {
        topics.value = topics.value.filter(t => t.id !== id);
    }

    return { topics, addTopic, removeTopic };
});
