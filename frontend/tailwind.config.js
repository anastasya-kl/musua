/** @type {import('tailwindcss').Config} */

const plugin = require('tailwindcss-react-native/plugin');

module.exports = {
  content: ["./app/**/*.{js,jsx,ts,tsx}", "./components/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        white: '#ffffff',
        backg: '#0C101F',
        blue: '#6496E7',
        gray: {
          100: '#9D9D9D',
          200: '#CDCDE0'
        },
        dark: '#04071B',
        purple: '#4510AF',
        black: {
          DEFAULT: "#000",
          100: "#1E1E2D",
          200: "#232533",
        },
        pink: "#CFAAFF",
        grad: "#211932",
        linearGradient1: ['#211932','#04071B'],
        linearGradient2: ['#04071B', '#211932'],
        
        transparent: 'rgba(0,0,0,0)',

      },
      fontFamily: {
        regular: ["NAMU1990"],
        medium: ["NAMU1750"]
      }
    },
  },
  plugins: [
    plugin,
  ],
}

