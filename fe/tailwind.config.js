/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        'soft-pink': '#fce7f3',
        'gray-muted': '#f3f4f6',
      }
    },
  },
  plugins: [],
}
