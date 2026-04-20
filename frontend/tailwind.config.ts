import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./features/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0F172A",
        muted: "#64748B",
        paper: "#F8FAFC",
        surface: "#FFFFFF",
        line: "#E2E8F0",
        primary: "#4F46E5",
        secondary: "#7C3AED",
        accent: "#06B6D4",
        success: "#10B981",
        warning: "#F59E0B",
        danger: "#EF4444",
        mint: "#10B981",
        coral: "#EF4444",
        amber: "#F59E0B"
      },
      boxShadow: {
        card: "0 1px 2px rgba(15, 23, 42, 0.04), 0 16px 32px -24px rgba(15, 23, 42, 0.24)",
        glow: "0 18px 40px -24px rgba(79, 70, 229, 0.55)"
      },
      fontFamily: {
        sans: ["Fira Sans", "Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["Fira Code", "ui-monospace", "SFMono-Regular", "Menlo", "monospace"]
      }
    }
  },
  plugins: []
};

export default config;
