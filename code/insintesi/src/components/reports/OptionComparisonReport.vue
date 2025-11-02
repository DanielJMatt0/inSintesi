<template>
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-x-6 gap-y-3 p-4">
    <ReportSection
      title="Topic"
      description="Main question analyzed by participants"
      class="rounded-xl border border-blue-200 bg-gradient-to-br from-blue-50/60 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <div>
        <p class="text-lg font-medium text-gray-800">
          {{ data.topic }}
        </p>
        <p class="text-sm text-gray-500 mt-1">
          Created: {{ formatDate(data.created_at) }} · Updated:
          {{ formatDate(data.updated_at) }}
        </p>
      </div>
    </ReportSection>
    <ReportSection
      title="Option Comparison"
      description="Comparison between available options and their support levels"
      class="row-span-2 rounded-xl border border-purple-300 bg-gradient-to-br from-purple-50/60 to-white shadow-sm p-5 hover:shadow-md transition-all flex flex-col items-center justify-center"
    >
      <div class="w-full max-h-[300px] h-[300px]">
        <Bar :data="chartData" :options="chartOptions" />
      </div>
      <p class="mt-4 text-sm text-gray-500 text-center">
        Total responses: {{ data.total_responses }}
      </p>
    </ReportSection>
    <ReportSection
      v-if="data.summary"
      title="Summary"
      class="rounded-xl border border-gray-200 bg-gradient-to-br from-gray-50 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <div
        class="prose max-w-none text-gray-800"
        v-html="renderMarkdown(data.summary)"
      />
    </ReportSection>
    <ReportSection
      v-if="hasReasons"
      title="Reasons Behind Choices"
      description="Key arguments and reasoning behind option preferences"
      class="col-span-1 lg:col-span-2 rounded-xl border border-green-300 bg-gradient-to-br from-green-50/60 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <div class="space-y-4">
        <div
          v-for="(reasons, option) in data.reasons"
          :key="option"
          class="bg-white rounded-lg p-4 border border-gray-200"
        >
          <p class="font-semibold text-gray-800 mb-2">{{ option }}</p>
          <ul class="list-disc pl-6 text-sm text-gray-700 space-y-1">
            <li v-for="(reason, i) in reasons" :key="i">{{ reason }}</li>
          </ul>
        </div>
      </div>
    </ReportSection>
    <ReportSection
      v-if="data.recommendation"
      title="Recommendation"
      class="col-span-1 lg:col-span-2 rounded-xl border border-gray-200 bg-gradient-to-br from-gray-50 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <div
        class="prose max-w-none"
        v-html="renderMarkdown(data.recommendation)"
      />
    </ReportSection>
    <ReportSection
      v-if="data.ai_thought"
      title="AI Thought"
      description="Internal reasoning trace of the AI model"
      class="col-span-1 lg:col-span-2 rounded-xl border border-gray-200 bg-gradient-to-br from-gray-50 to-white shadow-sm p-5 hover:shadow-md transition-all"
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

/* Chart data */
const chartData = computed(() => {
  const dist = props.data.distribution_and_options || {};
  const options = dist.options || [];
  const votes = dist.votes || {};
  return {
    labels: options,
    datasets: [
      {
        label: null,
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
    title: { display: true, text: "Option Comparison Results" },
    tooltip: {
      callbacks: {
        title: (ctx) => ctx[0]?.label ?? "",
        label: (ctx) => {
          const label = ctx.dataset.label || "Support";
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
    y: { beginAtZero: true },
  },
};

/* Check if reasons exist */
const hasReasons = computed(() => {
  const reasons = props.data.reasons;
  return (
    reasons && typeof reasons === "object" && Object.keys(reasons).length > 0
  );
});
</script>
