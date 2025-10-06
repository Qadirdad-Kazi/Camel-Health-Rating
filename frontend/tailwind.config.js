/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        camel: {
          50: '#fdf6e3',
          100: '#fcecc7',
          200: '#f8d68f',
          300: '#f4c057',
          400: '#f0aa1f',
          500: '#e69400',
          600: '#d17a00',
          700: '#b85c00',
          800: '#9f3e00',
          900: '#862000',
        },
        desert: {
          50: '#faf7f0',
          100: '#f5ede0',
          200: '#ead9c1',
          300: '#dfc5a2',
          400: '#d4b183',
          500: '#c99d64',
          600: '#b88a4a',
          700: '#97723c',
          800: '#765a2e',
          900: '#554220',
        }
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'bounce-slow': 'bounce 2s infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        }
      }
    },
  },
  plugins: [],
}
