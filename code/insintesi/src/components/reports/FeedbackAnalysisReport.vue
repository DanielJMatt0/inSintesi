<template>
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-x-6 gap-y-3 p-4">

    <ReportSection
      title="Topic"
      description="Main question or feedback theme analyzed"
      class="rounded-xl border border-gray-200 bg-gradient-to-br from-gray-50 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <div>
        <p class="text-lg font-medium text-gray-800">{{ data.topic }}</p>
        <p class="text-sm text-gray-500 mt-1">
          Created: {{ formatDate(data.created_at) }} · Updated:
          {{ formatDate(data.updated_at) }}
        </p>
      </div>
    </ReportSection>

    <ReportSection
      title="Sentiment Overview"
      description="Overall sentiment score based on participant feedback"
      class="rounded-xl border border-green-300 bg-gradient-to-br from-green-50/60 to-white shadow-sm p-5 flex items-center justify-center hover:shadow-md transition-all"
    >
      <div class="flex flex-col items-center justify-center py-3">
        <div class="text-5xl font-bold" :class="sentimentColor">
          {{ sentimentLabel }}
        </div>
        <p class="text-gray-500 mt-2">Score: {{ data.sentiment }}</p>
      </div>
    </ReportSection>

    <ReportSection
      v-if="hasPositive"
      title="Positive Themes"
      description="Highlights and strengths from feedback"
      class="col-span-1 lg:col-span-2 rounded-xl border border-green-300 bg-gradient-to-br from-green-50/50 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <ul class="grid grid-cols-1 md:grid-cols-2 gap-3">
        <li
          v-for="(theme, index) in positiveThemes"
          :key="'pos-' + index"
          class="bg-white rounded-lg p-3 border border-green-100 hover:bg-green-50/50 hover:shadow transition"
        >
          <p class="font-semibold text-green-700">{{ theme.name }}</p>
          <ul
            v-if="theme.examples && theme.examples.length"
            class="list-disc pl-6 text-sm text-gray-700 mt-1"
          >
            <li v-for="(ex, i) in theme.examples" :key="i">{{ ex }}</li>
          </ul>
        </li>
      </ul>
    </ReportSection>

    <ReportSection
      v-if="hasNegative"
      title="Negative Themes"
      description="Common concerns or pain points"
      class="col-span-1 lg:col-span-2 rounded-xl border border-red-300 bg-gradient-to-br from-red-50/50 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <ul class="grid grid-cols-1 md:grid-cols-2 gap-3">
        <li
          v-for="(theme, index) in negativeThemes"
          :key="'neg-' + index"
          class="bg-white rounded-lg p-3 border border-red-100 hover:bg-red-50/50 hover:shadow transition"
        >
          <p class="font-semibold text-red-700">{{ theme.name }}</p>
          <ul
            v-if="theme.examples && theme.examples.length"
            class="list-disc pl-6 text-sm text-gray-700 mt-1"
          >
            <li v-for="(ex, i) in theme.examples" :key="i">{{ ex }}</li>
          </ul>
        </li>
      </ul>
    </ReportSection>

    <ReportSection
      v-if="data.summary"
      title="Summary"
      class="col-span-1 lg:col-span-2 rounded-xl border border-gray-200 bg-gradient-to-br from-gray-50 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <div class="prose max-w-none" v-html="renderMarkdown(data.summary)" />
    </ReportSection>

    <ReportSection
      v-if="data.recommendation"
      title="Recommendation"
      class="col-span-1 lg:col-span-2 rounded-xl border border-gray-200 bg-gradient-to-br from-gray-50 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <div
        class="prose max-w-none"
        v-html="renderMarkdown(data.recommendation)"
      />
    </ReportSection>

    <ReportSection
      v-if="data.ai_thought"
      title="AI Thought"
      description="Internal reasoning trace of the AI model"
      class="col-span-1 lg:col-span-2 rounded-xl border border-gray-200 bg-gradient-to-br from-gray-50 to-white shadow-sm p-5 hover:shadow-md transition-all"
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
const props = defineProps({ data: { type: Object, required: true } });

/* Sentiment label and color */
const sentimentLabel = computed(() => {
  const s = props.data.sentiment;
  if (s > 0) return "Positive";
  if (s < 0) return "Negative";
  return "Neutral";
});
const sentimentColor = computed(() => {
  const s = props.data.sentiment;
  if (s > 0) return "text-green-600";
  if (s < 0) return "text-red-600";
  return "text-gray-600";
});
const positiveThemes = computed(() => props.data.positive_themes || []);
const negativeThemes = computed(() => props.data.negative_themes || []);
/* Check for themes */
const hasPositive = computed(() => {
  const t = props.data.positive_themes;
  return t && typeof t === "object" && Object.keys(t).length > 0;
});
const hasNegative = computed(() => {
  const t = props.data.negative_themes;
  return t && typeof t === "object" && Object.keys(t).length > 0;
});
</script>
