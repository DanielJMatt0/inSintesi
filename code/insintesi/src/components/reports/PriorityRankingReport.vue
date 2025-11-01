<template>
  <div>
    <!-- Topic -->
    <ReportSection title="Topic" description="Main question analyzed by participants">
      <div>
        <p class="text-lg font-medium text-gray-800">{{ data.topic }}</p>
        <p class="text-sm text-gray-500 mt-1">
          Created: {{ formatDate(data.created_at) }} · Updated: {{ formatDate(data.updated_at) }}
        </p>
      </div>
    </ReportSection>

    <!-- Priority Ranking -->
    <ReportSection
      title="Priority Ranking"
      description="Average ranking or importance score for each option"
    >
      <div class="h-64">
        <Bar :data="chartData" :options="chartOptions" />
      </div>

      <p class="mt-4 text-sm text-gray-500">
        Higher bars indicate higher priority scores.
      </p>
    </ReportSection>


    <!-- Top Reasons -->
    <ReportSection
      v-if="hasReasons"
      title="Top Reasons"
      description="Key explanations behind the prioritization"
    >
      <div class="space-y-4">
        <div
          v-for="(reasons, topic) in data.top_reasons"
          :key="topic"
          class="bg-gray-50 rounded-lg p-4 border border-gray-200"
        >
          <p class="font-semibold text-gray-800 mb-2">{{ topic }}</p>
          <ul class="list-disc pl-6 text-sm text-gray-700 space-y-1">
            <li v-for="(reason, i) in reasons" :key="i">{{ reason }}</li>
          </ul>
        </div>
      </div>
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
    <ReportSection v-if="data.ai_thought" title="AI Thought" description="Internal reasoning trace">
       <div v-html="renderMarkdown(data.ai_thought)" class="prose max-w-none"></div>
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
  data: { type: Object, required: true }
})

/* Chart data for ranking */
const chartData = computed(() => {
  console.log('options_and_means:', props.data.options_and_means)

  const dist = props.data.options_and_means || {}
  const options = dist.options || []
  const votes = dist.average_ranking || {}
  return {
    labels: options,
    datasets: [
      {
        label: 'Average Priority Score',
        data: options.map(opt => votes[opt] ?? 0),
      }
    ]
  }
})

/* Chart options */
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    title: { display: true, text: 'Stance Distribution' },
    tooltip: {
      callbacks: {
        title: (ctx) => ctx[0]?.label ?? '',
        label: (ctx) => {
          const label = ctx.dataset.label || 'Responses'
          const value = ctx.parsed.y ?? ctx.parsed
          return `${label}: ${value}`
        },
        afterLabel: (ctx) => {
          const total =
            ctx.chart.data.datasets[0].data.reduce((a, b) => a + b, 0) || 0
          const pct =
            total > 0 ? ((ctx.parsed.y / total) * 100).toFixed(1) + '%' : ''
          return pct
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: { precision: 0 }
    }
  }
}


/* Check for top reasons */
const hasReasons = computed(() => {
  const reasons = props.data.top_reasons
  return reasons && typeof reasons === 'object' && Object.keys(reasons).length > 0
})
</script>
