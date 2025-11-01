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
    <ReportSection
      v-if="hasPositive"
      title="Positive Themes"
      description="Highlights and strengths from feedback"
    >
      <ul class="space-y-3">
        <li
          v-for="(theme, index) in positiveThemes"
          :key="'pos-' + index"
          class="bg-green-50 rounded-lg p-3 border border-green-100"
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

    <!-- Negative Themes -->
    <ReportSection
      v-if="hasNegative"
      title="Negative Themes"
      description="Common concerns or pain points"
    >
      <ul class="space-y-3">
        <li
          v-for="(theme, index) in negativeThemes"
          :key="'neg-' + index"
          class="bg-red-50 rounded-lg p-3 border border-red-100"
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


    <!-- Summary -->
    <ReportSection v-if="data.summary" title="Summary">
       <div v-html="renderMarkdown(data.summary)" class="prose max-w-none"></div>
    </ReportSection>

    <!-- Recommendation -->
    <ReportSection v-if="data.recommendation" title="Recommendation">
       <div v-html="renderMarkdown(data.recommendation)" class="prose max-w-none"></div>
    </ReportSection>

    <!-- AI Thought -->
    <ReportSection
      v-if="data.ai_thought"
      title="AI Thought"
      description="Internal reasoning trace of the AI model"
    >
      
       <div v-html="renderMarkdown(data.ai_thought)" class="prose max-w-none"></div>
    </ReportSection>
  </div>
</template>

<script setup>
import ReportSection from '../ReportSection.vue'
import { formatDate, useMarkdown } from '../../utils/formatters'
import { computed } from 'vue'

const { renderMarkdown } = useMarkdown()

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

const positiveThemes = computed(() =>
  props.data.positive_themes ||
  []
)

const negativeThemes = computed(() =>
  props.data.negative_themes ||
  []
)


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
