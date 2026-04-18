import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./features/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#111827",
        paper: "#f8fafc",
        line: "#d1d5db",
        mint: "#0f766e",
        coral: "#be123c",
        amber: "#a16207"
      }
    }
  },
  plugins: []
};

export default config;
