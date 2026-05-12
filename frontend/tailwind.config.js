export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["'DM Serif Display'", "Georgia", "serif"],
        body: ["'DM Sans'", "system-ui", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      colors: {
        pharma: {
          50:  "#f0f7ff",
          100: "#e0effe",
          200: "#bae0fd",
          300: "#7cc8fb",
          400: "#36aaf5",
          500: "#0c90e1",
          600: "#0071bf",
          700: "#015a9a",
          800: "#064d7f",
          900: "#0b4169",
          950: "#072946",
        },
        accent: {
          DEFAULT: "#00c896",
          dark:    "#00a87c",
        }
      },
    },
  },
  plugins: [],
}
