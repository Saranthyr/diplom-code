/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        "custom-lightblue": "#F3F8FA",
        "custom-gray": "#95989A",
      },
      backgroundImage: {
        "custom-bg": "url('/background.png')",
      },
    },
  },
  plugins: [],
};
