import { defineStore } from 'pinia';

export const useTopicStore = defineStore('topics', {
    state: () => ({
        topics: [
            {
                id: 1,
                title: 'Should our team adopt the new AI tool?',
                responses: [{ user: 'John' }, { user: 'Maria' }],
            },
            {
                id: 2,
                title: 'What features should we prioritize in the next release?',
                responses: [{ user: 'David' }],
            },
        ],
    }),
    actions: {
        addTopic(title: string) {
            const newTopic = {
                id: Date.now(),
                title,
                responses: [],
            };
            this.topics.push(newTopic);
        },
        removeTopic(id: number) {
            this.topics = this.topics.filter((t) => t.id !== id);
        },
    },
});
