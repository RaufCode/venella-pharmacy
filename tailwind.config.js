/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        styleScript: ["Style Script", 'cursive'],
        montserrat: ["Montserrat"],
      },
    },
  },
  plugins: [],
}