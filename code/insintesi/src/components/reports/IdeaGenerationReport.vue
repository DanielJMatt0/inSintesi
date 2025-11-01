<template>
  <div>
    <!-- Topic -->
    <ReportSection title="Topic" description="Main subject of the idea generation process">
      <div>
        <p class="text-lg font-medium text-gray-800">
          {{ data.topic }}
        </p>
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
      <div class="space-y-4">
        <div
          v-for="(theme, index) in data.themes"
          :key="index"
          class="bg-gray-50 rounded-lg p-4 border border-gray-200"
        >
          <!-- Theme name -->
          <p class="font-semibold text-gray-800">
            {{ theme.name }}
          </p>

          <!-- Summary -->
          <p v-if="theme.summary"
class="text-sm text-gray-600 mt-1">
            {{ theme.summary }}
          </p>

          <!-- Ideas -->
          <ul
            v-if="theme.ideas && theme.ideas.length"
            class="list-disc pl-6 text-sm text-gray-700 mt-2"
          >
            <li v-for="(idea, i) in theme.ideas"
:key="i">
              {{ idea }}
            </li>
          </ul>
        </div>
      </div>
    </ReportSection>

    <!-- Summary -->
    <ReportSection
      v-if="data.summary"
      title="Summary"
      description="AI-generated synthesis of all ideas"
    >
      <div class="prose max-w-none"
v-html="renderMarkdown(data.summary)"
/>
    </ReportSection>

    <!-- Recommendation -->
    <ReportSection
      v-if="data.recommendation"
      title="Recommendation"
      description="Suggested next steps or actions based on generated ideas"
    >
      <div class="prose max-w-none"
v-html="renderMarkdown(data.recommendation)"
/>
    </ReportSection>

    <!-- AI Thought -->
    <ReportSection
      v-if="data.ai_thought"
      title="AI Thought"
      description="Internal reasoning trace of the AI model"
    >
      <div class="prose max-w-none"
v-html="renderMarkdown(data.ai_thought)"
/>
    </ReportSection>
  </div>
</template>

<script setup>
import ReportSection from '../ReportSection.vue'
import { formatDate, useMarkdown } from '../../utils/formatters'
import { computed } from 'vue'

const { renderMarkdown } = useMarkdown()

const props = defineProps({
  data: { type: Object, required: true },
})

const hasThemes = computed(() => {
  const themes = props.data.themes
  return themes && typeof themes === 'object' && Object.keys(themes).length > 0
})
</script>
