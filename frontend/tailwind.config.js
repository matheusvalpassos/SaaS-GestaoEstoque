/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // Caminho para os templates Django (agora relativos à pasta 'frontend')
    // Sobe um nível (para 'meu_saas_projeto/'), entra em 'backend/', 'core/', 'templates/'
    '../backend/core/templates/**/*.html',

    // Caminho para arquivos JavaScript e HTML dentro da pasta 'static_dev'
    // (que está dentro de 'backend/')
    '../backend/static_dev/**/*.js',
    '../backend/static_dev/**/*.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
  safelist: [
    'min-w-[70px]',
    'bg-green-100',
    'text-green-800',
    'bg-yellow-100',
    'text-yellow-800',
    'bg-red-100',
    'text-red-800',
  ],
}