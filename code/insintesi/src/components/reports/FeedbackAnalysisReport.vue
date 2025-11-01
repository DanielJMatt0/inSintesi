<template>
  <div>
    <!-- Topic -->
    <ReportSection title="Topic" description="Main question or feedback theme analyzed">
      <div>
        <p class="text-lg font-medium text-gray-800">{{ data.topic }}</p>
        <p class="text-sm text-gray-500 mt-1">
          Created: {{ formatDate(data.created_at) }} · Updated: {{ formatDate(data.updated_at) }}
        </p>
      </div>
    </ReportSection>

    <!-- Sentiment Overview -->
    <ReportSection title="Sentiment Overview" description="Overall sentiment score based on participant feedback">
      <div class="flex flex-col items-center justify-center py-4">
        <div
          class="text-5xl font-bold"
          :class="sentimentColor"
        >
          {{ sentimentLabel }}
        </div>
        <p class="text-gray-500 mt-2">Score: {{ data.sentiment }}</p>
      </div>
    </ReportSection>

    <!-- Positive Themes -->
    <ReportSection v-if="hasPositive" title="Positive Themes" description="Highlights and strengths from feedback">
      <ul class="list-disc pl-6 space-y-1">
        <li v-for="(value, key) in data.positive_themes" :key="key">
          <strong>{{ key }}:</strong> {{ value }}
        </li>
      </ul>
    </ReportSection>

    <!-- Negative Themes -->
    <ReportSection v-if="hasNegative" title="Negative Themes" description="Common concerns or pain points">
      <ul class="list-disc pl-6 space-y-1">
        <li v-for="(value, key) in data.negative_themes" :key="key">
          <strong>{{ key }}:</strong> {{ value }}
        </li>
      </ul>
    </ReportSection>

    <!-- Summary -->
    <ReportSection v-if="data.summary" title="Summary">
      <p class="whitespace-pre-line">{{ data.summary }}</p>
    </ReportSection>

    <!-- Recommendation -->
    <ReportSection v-if="data.recommendation" title="Recommendation">
      <p class="whitespace-pre-line">{{ data.recommendation }}</p>
    </ReportSection>

    <!-- AI Thought -->
    <ReportSection
      v-if="data.ai_thought"
      title="AI Thought"
      description="Internal reasoning trace of the AI model"
    >
      <pre
        class="bg-gray-50 rounded-xl p-4 overflow-auto text-sm whitespace-pre-wrap text-gray-700"
      >
{{ data.ai_thought }}
      </pre>
    </ReportSection>
  </div>
</template>

<script setup>
import ReportSection from '@/components/ReportSection.vue'
import { formatDate } from '@/utils/formatters'
import { computed } from 'vue'

const props = defineProps({
  data: { type: Object, required: true }
})

/* Sentiment label and color */
const sentimentLabel = computed(() => {
  const s = props.data.sentiment
  if (s > 0) return 'Positive'
  if (s < 0) return 'Negative'
  return 'Neutral'
})

const sentimentColor = computed(() => {
  const s = props.data.sentiment
  if (s > 0) return 'text-green-600'
  if (s < 0) return 'text-red-600'
  return 'text-gray-600'
})

/* Check for themes */
const hasPositive = computed(() => {
  const t = props.data.positive_themes
  return t && typeof t === 'object' && Object.keys(t).length > 0
})

const hasNegative = computed(() => {
  const t = props.data.negative_themes
  return t && typeof t === 'object' && Object.keys(t).length > 0
})
</script>
