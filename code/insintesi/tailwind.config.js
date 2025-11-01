export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: '#2563eb',
          light: '#3b82f6',
          dark: '#1e3a8a',
        },
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
}
