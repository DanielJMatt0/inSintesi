<template>
  <div class="p-6">
    <h1 class="text-3xl font-bold mb-6">Report</h1>

    <div v-if="loading" class="text-gray-500">Loading report...</div>
    <div v-if="error" class="text-red-500">{{ error }}</div>

    <component
      v-if="report && componentName"
      :is="componentName"
      :data="report"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

import StanceReport from '../components/reports/StanceReport.vue'
import OptionComparisonReport from '../components/reports/OptionComparisonReport.vue'
import IdeaGenerationReport from '../components/reports/IdeaGenerationReport.vue'
import PriorityRankingReport from '../components/reports/PriorityRankingReport.vue'
import FeedbackAnalysisReport from '../components/reports/FeedbackAnalysisReport.vue'

const props = defineProps({
  questionId: Number
})

const loading = ref(true)
const error = ref(null)
const report = ref(null)
const reportType = ref(null)

const components = {
  stance_analysis: StanceReport,
  option_comparison: OptionComparisonReport,
  idea_generation: IdeaGenerationReport,
  priority_ranking: PriorityRankingReport,
  feedback_analysis: FeedbackAnalysisReport
}

const componentName = computed(() => components[reportType.value] || null)

onMounted(async () => {
  try {
    // TODO
    const res = await fetch(`http://10.197.135.91:8000/analyze/report/${props.questionId}`)
    if (!res.ok) throw new Error('Error while loading report')
    const data = await res.json()
    console.log(data)

    report.value = data
    reportType.value = data.type
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
})
</script>
