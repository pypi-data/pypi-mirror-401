import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    define: {
        'process.env': {} // Fixes potential process.env usage in dependencies
    },
    build: {
        outDir: 'dist/embed',
        lib: {
            entry: path.resolve(__dirname, 'src/embed.tsx'),
            name: 'EpistWidgetEmbed',
            fileName: () => `epist-widget.js`,
            formats: ['umd']
        },
        rollupOptions: {
            // Do NOT externalize React here, we want it bundled for the standalone script
            external: [],
            output: {
                // No globals needed as everything is bundled
            }
        },
        emptyOutDir: true
    }
})
