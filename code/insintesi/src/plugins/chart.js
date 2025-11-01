import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  PointElement,
  LineElement
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  PointElement,
  LineElement
)

ChartJS.defaults.color = '#1f2937' // Tailwind gray-800
ChartJS.defaults.font.family = 'Inter, system-ui, sans-serif'
ChartJS.defaults.font.size = 13
ChartJS.defaults.plugins.legend.position = 'bottom'
ChartJS.defaults.plugins.title.font = { weight: '600', size: 16 }
ChartJS.defaults.plugins.tooltip.cornerRadius = 8
ChartJS.defaults.plugins.tooltip.padding = 10
ChartJS.defaults.plugins.tooltip.backgroundColor = 'rgba(31, 41, 55, 0.9)'
ChartJS.defaults.plugins.tooltip.titleColor = '#fff'
ChartJS.defaults.plugins.tooltip.bodyColor = '#f9fafb'

export { ChartJS }
