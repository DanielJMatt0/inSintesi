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
      title="Opinion Distribution"
      description="Distribution of participant stances (Pro / Contra / Neutral)"
      class="row-span-2 rounded-xl border border-purple-300 bg-gradient-to-br from-purple-50/60 to-white shadow-sm p-5 hover:shadow-md transition-all flex flex-col justify-center"
    >
      <Bar :data="chartData" :options="chartOptions" />
      <p class="mt-4 text-sm text-gray-500 text-center">
        Total responses: {{ data.total_responses }}
      </p>
    </ReportSection>
    <ReportSection
      v-if="data.summary"
      title="Summary"
      class="rounded-xl border border-gray-200 bg-gradient-to-br from-gray-50 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <div class="prose max-w-none text-gray-800" v-html="renderMarkdown(data.summary)" />
    </ReportSection>
    <ReportSection
      v-if="hasThemes"
      title="Key Themes"
      description="Main themes identified from participants' comments"
      class="col-span-1 lg:col-span-2 rounded-xl border border-green-300 bg-gradient-to-br from-green-50/60 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <ul class="list-disc pl-6 space-y-1">
        <li v-for="(value, key) in data.themes" :key="key">
          <strong class="text-green-700">{{ key }}:</strong> {{ value }}
        </li>
      </ul>
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
      class="col-span-1 lg:col-span-2 rounded-xl border border-gray-200 bg-gradient-to-br from-gray-50 to-white shadow-sm p-5 hover:shadow-md transition-all"
    >
      <div class="prose max-w-none" v-html="renderMarkdown(data.ai_thought)" />
    </ReportSection>
  </div>
</template>

<script setup lang="ts">
import ReportSection from "../ReportSection.vue";
// @ts-ignore
import { formatDate, useMarkdown } from "../../utils/formatters";
import { computed } from "vue";
import { Bar } from "vue-chartjs";
import "@/plugins/chart.js";

const { renderMarkdown } = useMarkdown();

const props = defineProps({
  data: { type: Object, required: true },
});

const chartData = computed(() => {
  const dist = props.data.distribution || {};
  return {
    labels: Object.keys(dist),
    datasets: [
      {
        label: "Responses",
        data: Object.values(dist),
        backgroundColor: [
          "rgba(34, 197, 94, 0.8)",   // 🟩 Pro (green-500)
          "rgba(239, 68, 68, 0.8)",   // 🟥 Contra (red-500)
          "rgba(234, 179, 8, 0.8)",   // 🟨 Neutral (yellow-500)
        ],
        borderColor: [
          "rgb(34, 197, 94)",
          "rgb(239, 68, 68)",
          "rgb(234, 179, 8)",
        ],
      },
    ],
  };
});

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { display: false },
    title: { display: true, text: "Stance Distribution" },
  },
};

const hasThemes = computed(() => {
  const th = props.data.themes;
  return th && typeof th === "object" && Object.keys(th).length > 0;
});
</script>
