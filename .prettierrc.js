module.exports = {
    singleQuote: true,
    printWidth: 120,
    eslintIntegration: true,
    tabWidth: 4,
    plugins: ['prettier-plugin-tailwindcss'],
    endOfLine: 'auto',
    trailingComma: 'all',
    overrides: [
        {
            files: ['*.yml', '*.yaml'],
            options: {
                tabWidth: 4,
            },
        },
    ],
};
