<template>
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-x-6 gap-y-3 p-4">
    <ReportSection
      title="Topic"
      description="Main subject of the idea generation process"
      class="col-span-1 lg:col-span-2 rounded-xl border border-blue-200 bg-gradient-to-br from-blue-50/60 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <div>
        <p class="text-lg font-medium text-gray-800">
          {{ data.topic }}
        </p>
        <p class="text-sm text-gray-500 mt-1">
          Created: {{ formatDate(data.created_at) }} · Updated:
          {{ formatDate(data.updated_at) }}
        </p>
      </div>
    </ReportSection>
    <ReportSection
      v-if="hasThemes"
      title="Generated Themes"
      description="Clusters of related ideas or key topics derived from participant input"
      class="row-span-2 rounded-xl border border-green-300 bg-gradient-to-br from-green-50/60 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <div class="space-y-4">
        <div
          v-for="(theme, index) in data.themes"
          :key="index"
          class="bg-white rounded-lg p-4 border border-green-100 shadow-sm hover:shadow-md transition"
        >
          <p class="font-semibold text-green-700">
            {{ theme.name }}
          </p>
          <p v-if="theme.summary" class="text-sm text-gray-600 mt-1">
            {{ theme.summary }}
          </p>
          <ul
            v-if="theme.ideas && theme.ideas.length"
            class="list-disc pl-6 text-sm text-gray-700 mt-2 space-y-1"
          >
            <li v-for="(idea, i) in theme.ideas" :key="i">
              {{ idea }}
            </li>
          </ul>
        </div>
      </div>
    </ReportSection>
    <ReportSection
      v-if="data.summary"
      title="Summary"
      description="AI-generated synthesis of all ideas"
      class="rounded-xl border border-gray-200 bg-gradient-to-br from-gray-50 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <div class="prose max-w-none text-gray-800" v-html="renderMarkdown(data.summary)" />
    </ReportSection>
    <ReportSection
      v-if="data.recommendation"
      title="Recommendation"
      description="Suggested next steps or actions based on generated ideas"
      class="rounded-xl border border-gray-200 bg-gradient-to-br from-gray-50 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <div class="prose max-w-none text-gray-800" v-html="renderMarkdown(data.recommendation)" />
    </ReportSection>
    <ReportSection
      v-if="data.ai_thought"
      title="AI Thought"
      description="Internal reasoning trace of the AI model"
      class="col-span-1 lg:col-span-2 rounded-xl border border-indigo-200 bg-gradient-to-br from-indigo-50/60 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <div class="prose max-w-none" v-html="renderMarkdown(data.ai_thought)" />
    </ReportSection>
  </div>
</template>

<script setup lang="ts">
import ReportSection from "../ReportSection.vue";
import { formatDate, useMarkdown } from "../../utils/formatters";
import { computed } from "vue";

const { renderMarkdown } = useMarkdown();

const props = defineProps({
  data: { type: Object, required: true },
});

const hasThemes = computed(() => {
  const themes = props.data.themes;
  return themes && typeof themes === "object" && Object.keys(themes).length > 0;
});
</script>
