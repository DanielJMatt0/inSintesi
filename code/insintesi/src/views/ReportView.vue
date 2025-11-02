<template>
  <div class="p-6">
    <div v-if="loading" class="text-gray-500">Loading report...</div>
    <div v-if="error" class="text-red-500">
      {{ error }}
    </div>

    <component
      :is="componentName"
      v-if="report && componentName"
      :data="report"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router"

import StanceReport from "../components/reports/StanceReport.vue";
import OptionComparisonReport from "../components/reports/OptionComparisonReport.vue";
import IdeaGenerationReport from "../components/reports/IdeaGenerationReport.vue";
import PriorityRankingReport from "../components/reports/PriorityRankingReport.vue";
import FeedbackAnalysisReport from "../components/reports/FeedbackAnalysisReport.vue";
import { getReport } from "@/api/analysis";

const route = useRoute()
const questionId = Number(route.params.questionId) 
console.log(questionId)

const loading = ref(true);
const error = ref(null);
const report = ref(null);
const reportType = ref(null);

const components = {
  stance_analysis: StanceReport,
  option_comparison: OptionComparisonReport,
  idea_generation: IdeaGenerationReport,
  priority_ranking: PriorityRankingReport,
  feedback_analysis: FeedbackAnalysisReport,
};

// @ts-ignore
const componentName = computed(() => components[reportType.value] || null);

onMounted(async () => {
  try {
    // TODO
    const data = await getReport(questionId)
    console.log("Report data:", data)


    report.value = data;
    reportType.value = data.type;
  } catch (err) {
    // @ts-ignore
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});
</script>
