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
      <Bar :data="chartData" :options="chartOptions" />
      <p class="mt-4 text-sm text-gray-500">Higher bars indicate higher priority scores.</p>
    </ReportSection>

    <!-- Top Reasons -->
    <ReportSection
      v-if="hasReasons"
      title="Top Reasons"
      description="Key explanations behind the prioritization"
    >
      <ul class="list-disc pl-6 space-y-1">
        <li v-for="(value, key) in data.top_reasons" :key="key">
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
    <ReportSection v-if="data.ai_thought" title="AI Thought" description="Internal reasoning trace">
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
import { Bar } from 'vue-chartjs'
import { ChartJS } from '@/plugins/chart'

const props = defineProps({
  data: { type: Object, required: true }
})

/* Chart data for ranking */
const chartData = computed(() => {
  const dist = props.data.options_and_means || {}
  return {
    labels: Object.keys(dist),
    datasets: [
      {
        label: 'Average Priority Score',
        data: Object.values(dist)
      }
    ]
  }
})

/* Chart options */
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'bottom' },
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
