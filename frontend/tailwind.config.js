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
    screens: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    '2lg': '1440px',
    xl: '1280px',
    '2xl': '1536px',
  },
    
  },
  plugins: [],
}