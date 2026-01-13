const fs = require('fs');
const path = require('path');

// Configuration
const API_KEY = process.env.EPIST_API_KEY || 'sk_live_replace_me';
const BASE_URL = 'https://api.epist.ai/v1';

async function uploadAudio(filePath) {
    console.log(`Uploading ${filePath}...`);

    // Create FormData with boundary
    const formData = new FormData();
    const fileBuffer = fs.readFileSync(filePath);
    const blob = new Blob([fileBuffer]);
    formData.append('file', blob, path.basename(filePath));

    const response = await fetch(`${BASE_URL}/audio/upload`, {
        method: 'POST',
        headers: {
            'X-API-Key': API_KEY,
            // Note: fetch automatically sets Content-Type to multipart/form-data with boundary
        },
        body: formData
    });

    if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
    }

    return await response.json();
}

async function searchKnowledgeBase(query) {
    console.log(`\nSearching for: '${query}'`);

    const response = await fetch(`${BASE_URL}/search`, {
        method: 'POST',
        headers: {
            'X-API-Key': API_KEY,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            query: query,
            limit: 3,
            rrf_k: 60
        })
    });

    if (!response.ok) {
        throw new Error(`Search failed: ${response.statusText}`);
    }

    const results = await response.json();

    results.forEach((res, i) => {
        console.log(`${i + 1}. [${res.score.toFixed(2)}] ${res.text.substring(0, 100)}...`);
    });
}

async function main() {
    // 1. Upload
    const demoFile = 'demo_meeting.mp3';

    if (!fs.existsSync(demoFile)) {
        console.log('Please provide a real audio file path.');
        return;
    }

    try {
        const uploadRes = await uploadAudio(demoFile);
        console.log('Upload Response:', uploadRes);

        // Wait for processing (simplistic)
        await new Promise(resolve => setTimeout(resolve, 2000));

        // 2. Search
        await searchKnowledgeBase('roadmap Q3');

    } catch (error) {
        console.error('Error:', error);
    }
}

main();
