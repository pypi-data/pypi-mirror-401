import React from 'react';
import ReactDOM from 'react-dom/client';
import { AudioSearchWidget } from './AudioSearchWidget';

// Look for the container
const container = document.getElementById('epist-widget');

if (container) {
    const apiKey = container.getAttribute('data-api-key');
    const baseUrl = container.getAttribute('data-base-url') || undefined;
    const placeholder = container.getAttribute('data-placeholder') || undefined;
    const limit = container.getAttribute('data-limit');

    if (apiKey) {
        const root = ReactDOM.createRoot(container);
        root.render(
            <React.StrictMode>
                <AudioSearchWidget
                    apiKey={apiKey}
                    baseUrl={baseUrl}
                    placeholder={placeholder}
                    limit={limit ? parseInt(limit, 10) : undefined}
                />
            </React.StrictMode>
        );
    } else {
        console.error('Epist Widget: data-api-key attribute is missing on #epist-widget container.');
    }
}
