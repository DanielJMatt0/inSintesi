<template>
  <div>
    <!-- Topic -->
    <ReportSection
      title="Topic"
      description="Main question analyzed by participants"
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

    <!-- Option Distribution -->
    <ReportSection
      title="Option Comparison"
      description="Comparison between available options and their support levels"
    >
      <Bar :data="chartData" :options="chartOptions" />
    </ReportSection>

    <!-- Reasons -->
    <ReportSection
      v-if="hasReasons"
      title="Reasons Behind Choices"
      description="Key arguments and reasoning behind option preferences"
    >
      <div class="space-y-4">
        <div
          v-for="(reasons, option) in data.reasons"
          :key="option"
          class="bg-gray-50 rounded-lg p-4 border border-gray-200"
        >
          <p class="font-semibold text-gray-800 mb-2">
            {{ option }}
          </p>
          <ul class="list-disc pl-6 text-sm text-gray-700 space-y-1">
            <li v-for="(reason, i) in reasons" :key="i">
              {{ reason }}
            </li>
          </ul>
        </div>
      </div>
    </ReportSection>

    <!-- Summary -->
    <ReportSection v-if="data.summary" title="Summary">
      <div class="prose max-w-none" v-html="renderMarkdown(data.summary)" />
    </ReportSection>

    <!-- Recommendation -->
    <ReportSection v-if="data.recommendation" title="Recommendation">
      <div
        class="prose max-w-none"
        v-html="renderMarkdown(data.recommendation)"
      />
    </ReportSection>

    <!-- AI Thought -->
    <ReportSection
      v-if="data.ai_thought"
      title="AI Thought"
      description="Internal reasoning trace of the AI model"
    >
      <div class="prose max-w-none" v-html="renderMarkdown(data.ai_thought)" />
    </ReportSection>
  </div>
</template>

<script setup>
import ReportSection from "../ReportSection.vue";
import { formatDate, useMarkdown } from "../../utils/formatters";
import { computed } from "vue";
import { Bar } from "vue-chartjs";
import { ChartJS } from "../../plugins/chart";

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
