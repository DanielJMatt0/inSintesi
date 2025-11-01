<template>
  <div>
    <!-- Topic -->
    <ReportSection title="Topic" description="Main question analyzed by participants">
      <div>
        <p class="text-lg font-medium text-gray-800">
          {{ data.topic }}
        </p>
        <p class="text-sm text-gray-500 mt-1">
          Created: {{ formatDate(data.created_at) }} · Updated: {{ formatDate(data.updated_at) }}
        </p>
      </div>
    </ReportSection>

    <!-- Opinion Distribution -->
    <ReportSection
      title="Opinion Distribution"
      description="Distribution of participant stances (Pro / Contra / Neutral)"
    >
      <Bar :data="chartData"
:options="chartOptions" />
      <p class="mt-4 text-sm text-gray-500">
Total responses: {{ data.total_responses }}
</p>
    </ReportSection>

    <!-- Themes -->
    <ReportSection
      v-if="hasThemes"
      title="Key Themes"
      description="Main themes identified from participants' comments"
    >
      <ul class="list-disc pl-6 space-y-1">
        <li v-for="(value, key) in data.themes"
:key="key">
          <strong>{{ key }}:</strong> {{ value }}
        </li>
      </ul>
    </ReportSection>

    <!-- Summary -->
    <ReportSection v-if="data.summary"
title="Summary">
      <!-- <p class="whitespace-pre-line">{{ data.summary }}</p> -->
      <div class="prose max-w-none"
v-html="renderMarkdown(data.summary)"
/>
    </ReportSection>

    <!-- Recommendation -->
    <ReportSection v-if="data.recommendation"
title="Recommendation">
      <!-- <p class="whitespace-pre-line">{{ data.recommendation }}</p> -->
      <div class="prose max-w-none"
v-html="renderMarkdown(data.recommendation)"
/>
    </ReportSection>

    <!-- AI Thought -->
    <ReportSection v-if="data.ai_thought"
title="AI Thought" description="Internal reasoning trace">
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
import { Bar } from 'vue-chartjs'
import { ChartJS } from '../../plugins/chart'

const { renderMarkdown } = useMarkdown()

const props = defineProps({
  data: { type: Object, required: true },
})

const chartData = computed(() => {
  const dist = props.data.distribution || {}
  return {
    labels: Object.keys(dist),
    datasets: [
      {
        label: 'Responses',
        data: Object.values(dist),
      },
    ],
  }
})

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { display: false },
    title: { display: true, text: 'Stance Distribution' },
  },
}

const hasThemes = computed(() => {
  const th = props.data.themes
  return th && typeof th === 'object' && Object.keys(th).length > 0
})
</script>
