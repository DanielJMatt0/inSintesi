<template>
  <div>
    <!-- Topic -->
    <ReportSection
        title="Topic"
        description="Main subject of the idea generation process"
    >
      <div>
        <p class="text-lg font-medium text-gray-800">{{ data.topic }}</p>
        <p class="text-sm text-gray-500 mt-1">
          Created: {{ formatDate(data.created_at) }} · Updated: {{ formatDate(data.updated_at) }}
        </p>
      </div>
    </ReportSection>

    <!-- Themes -->
    <ReportSection
      v-if="hasThemes"
      title="Generated Themes"
      description="Clusters of related ideas or key topics derived from participant input"
    >
      <ul class="list-disc pl-6 space-y-1">
        <li v-for="(value, key) in data.themes" :key="key">
          <strong>{{ key }}:</strong> {{ value }}
        </li>
      </ul>
    </ReportSection>

    <!-- Summary -->
    <ReportSection v-if="data.summary" title="Summary" description="AI-generated synthesis of all ideas">
      <p class="whitespace-pre-line">{{ data.summary }}</p>
    </ReportSection>

    <!-- Recommendation -->
    <ReportSection
      v-if="data.recommendation"
      title="Recommendation"
      description="Suggested next steps or actions based on generated ideas"
    >
      <p class="whitespace-pre-line">{{ data.recommendation }}</p>
    </ReportSection>

    <!-- AI Thought -->
    <ReportSection v-if="data.ai_thought" title="AI Thought" description="Internal reasoning trace of the AI model">
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

const props = defineProps({
  data: { type: Object, required: true }
})

const hasThemes = computed(() => {
  const themes = props.data.themes
  return themes && typeof themes === 'object' && Object.keys(themes).length > 0
})
</script>
