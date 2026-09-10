/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: { navy: '#1e293b', slate: '#334155', light: '#475569' },
        accent: { orange: '#f97316', 'orange-light': '#fdba74', blue: '#3b82f6', 'blue-light': '#93c5fd' },
        status: { success: '#22c55e', 'success-light': '#86efac', warning: '#f59e0b', 'warning-light': '#fcd34d', danger: '#ef4444', 'danger-light': '#fca5a5', info: '#3b82f6' }
      }
    }
  },
  plugins: []
}