/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "assets/templates/*.html",
        "src/splendor_bot/**/*.py",
    ],
    plugins: [
        require('@tailwindcss/container-queries'),
    ],
    theme: {},
}
