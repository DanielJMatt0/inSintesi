<template>
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-x-6 gap-y-3 p-4">
    <ReportSection
      title="Topic"
      description="Main question analyzed by participants"
      class="rounded-xl border border-blue-200 bg-gradient-to-br from-blue-50/60 to-white shadow-sm p-5 hover:shadow-md transition-all"
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
      title="Priority Ranking"
      description="Average ranking or importance score for each option"
      class="row-span-2 rounded-xl border border-purple-300 bg-gradient-to-br from-purple-50/60 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <div class="relative w-full h-[400px] lg:h-[460px]">
        <Bar
          :data="chartData"
          :options="chartOptions"
        />
      </div>

      <p class="mt-4 text-sm text-gray-500 text-center">
        Higher bars indicate higher priority scores.
      </p>
    </ReportSection>

    <ReportSection
      v-if="hasReasons"
      title="Top Reasons"
      description="Key explanations behind the prioritization"
      class="rounded-xl border border-green-300 bg-gradient-to-br from-green-50/60 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <div class="space-y-4">
        <div
          v-for="(reasons, topic) in data.top_reasons"
          :key="topic"
          class="bg-white rounded-lg p-4 border border-green-100 shadow-sm hover:shadow-md transition"
        >
          <p class="font-semibold text-green-700 mb-2">{{ topic }}</p>
          <ul class="list-disc pl-6 text-sm text-gray-700 space-y-1">
            <li v-for="(reason, i) in reasons" :key="i">{{ reason }}</li>
          </ul>
        </div>
      </div>
    </ReportSection>
    <ReportSection
      v-if="data.summary"
      title="Summary"
      class="col-span-1 lg:col-span-2 rounded-xl border border-gray-200 bg-gradient-to-br from-gray-50 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <div class="prose max-w-none text-gray-800" v-html="renderMarkdown(data.summary)" />
    </ReportSection>
    <ReportSection
      v-if="data.recommendation"
      title="Recommendation"
      class="col-span-1 lg:col-span-2 rounded-xl border border-gray-200 bg-gradient-to-br from-gray-50 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <div class="prose max-w-none" v-html="renderMarkdown(data.recommendation)" />
    </ReportSection>
    <ReportSection
      v-if="data.ai_thought"
      title="AI Thought"
      description="Internal reasoning trace"
      class="col-span-1 lg:col-span-2 rounded-xl border border-indigo-200 bg-gradient-to-br from-indigo-50/60 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <div class="prose max-w-none" v-html="renderMarkdown(data.ai_thought)" />
    </ReportSection>
  </div>
</template>

<script setup lang="ts">
import ReportSection from "../ReportSection.vue";
import { formatDate, useMarkdown } from "../../utils/formatters";
import { computed } from "vue";
import { Bar } from "vue-chartjs";
import "@/plugins/chart.js";

const { renderMarkdown } = useMarkdown();

const props = defineProps({
  data: { type: Object, required: true },
});

/* Chart data for ranking */
const chartData = computed(() => {
  console.log("options_and_means:", props.data.options_and_means);

  const dist = props.data.options_and_means || {};
  const options = dist.options || [];
  const votes = dist.average_ranking || {};
  return {
    labels: options,
    datasets: [
      {
        label: "Average Priority Score",
        data: options.map((opt) => votes[opt] ?? 0),
      },
    ],
  };
});

/* Chart options */
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    title: { display: true, text: "Stance Distribution" },
    tooltip: {
      callbacks: {
        title: (ctx) => ctx[0]?.label ?? "",
        label: (ctx) => {
          const label = ctx.dataset.label || "Responses";
          const value = ctx.parsed.y ?? ctx.parsed;
          return `${label}: ${value}`;
        },
        afterLabel: (ctx) => {
          const total =
            ctx.chart.data.datasets[0].data.reduce((a, b) => a + b, 0) || 0;
          const pct =
            total > 0 ? ((ctx.parsed.y / total) * 100).toFixed(1) + "%" : "";
          return pct;
        },
      },
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: { precision: 0 },
    },
  },
};

/* Check for top reasons */
const hasReasons = computed(() => {
  const reasons = props.data.top_reasons;
  return (
    reasons && typeof reasons === "object" && Object.keys(reasons).length > 0
  );
});
</script>
