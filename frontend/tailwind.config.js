/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        studio: {
          bg: "#0a0e17",
          panel: "#111827",
          border: "#1f2a3d",
          cyan: "#38bdf8",
          purple: "#a855f7",
        },
      },
    },
  },
  plugins: [],
};
