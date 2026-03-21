import {defineConfig} from 'vite';
import laravel, {refreshPaths} from 'laravel-vite-plugin';
import fs from 'fs';
import path from 'path';

const devHost = process.env.VITE_DEV_HOST || '__SHIPYARD_PROJECT_DOMAIN__';
const certDir = process.env.VITE_CERT_DIR || '/certs';

const httpsConfig = (() => {
    try {
        return {
            key: fs.readFileSync(path.join(certDir, `${devHost}-key.pem`)),
            cert: fs.readFileSync(path.join(certDir, `${devHost}.pem`)),
        };
    } catch (error) {
        console.warn(`[vite] HTTPS certs not found in ${certDir}, falling back to HTTP`);
        return false;
    }
})();

export default defineConfig({
    plugins: [
        laravel({
            input: [
                'resources/css/app.css',
                'resources/js/app.js',
            ],
            refresh: [
                ...refreshPaths,
                'app/Http/Livewire/**',
            ],
        }),
    ],
    server: {
        host: '0.0.0.0',
        port: 5173,
        strictPort: true,
        https: httpsConfig,
        allowedHosts: [
            devHost,
            'localhost',
        ],
        hmr: {
            host: devHost,
            protocol: httpsConfig ? 'wss' : 'ws',
            port: 5173,
        },
    },
});
