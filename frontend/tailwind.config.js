/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', '"Noto Sans Devanagari"', 'system-ui', 'sans-serif'],
      },
      colors: {
        agro: {
          yellow: {
            50:  '#fefce8',
            100: '#fef9c3',
            200: '#fef08a',
            300: '#fde047',
            400: '#facc15',
            500: '#eab308',
            600: '#ca8a04',
            700: '#a16207',
            800: '#854d0e',
            900: '#713f12',
          },
          green: {
            50:  '#f0fdf4',
            100: '#dcfce7',
            200: '#bbf7d0',
            300: '#86efac',
            400: '#4ade80',
            500: '#22c55e',
            600: '#16a34a',
            700: '#15803d',
            800: '#166534',
            900: '#14532d',
          },
        },
      },
      boxShadow: {
        'warm': '0 10px 30px -5px rgba(234, 179, 8, 0.15), 0 4px 6px -2px rgba(22, 163, 74, 0.05)',
        'warm-lg': '0 20px 40px -15px rgba(234, 179, 8, 0.25)',
      },
      backgroundImage: {
        'farm-light': 'linear-gradient(135deg, #ffffff 0%, #fefce8 60%, #f0fdf4 100%)',
        'yellow-gradient': 'linear-gradient(135deg, #facc15 0%, #eab308 100%)',
        'gold-green': 'linear-gradient(135deg, #eab308 0%, #16a34a 100%)',
      },
    },
  },
  plugins: [],
}
