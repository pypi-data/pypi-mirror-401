// Configuration
const API_KEY = process.env.EPIST_API_KEY || 'sk_live_replace_me';
const BASE_URL = 'https://api.epist.ai/v1';

async function chatRag(question) {
    console.log(`User: ${question}`);
    process.stdout.write('Assistant: ');

    const response = await fetch(`${BASE_URL}/chat/completions`, {
        method: 'POST',
        headers: {
            'X-API-Key': API_KEY,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            messages: [
                { role: 'system', content: 'You are a helpful assistant.' },
                { role: 'user', content: question }
            ],
            model: 'gpt-4-turbo',
            stream: true
        })
    });

    if (!response.ok) {
        throw new Error(`Chat failed: ${response.statusText}`);
    }

    // Handle Streaming Response
    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
            if (line.startsWith('data: ')) {
                const dataStr = line.replace('data: ', '');
                if (dataStr === '[DONE]') break;

                try {
                    const data = JSON.parse(dataStr);
                    const token = data.choices[0].delta.content || '';
                    process.stdout.write(token);
                } catch (e) {
                    // Ignore JSON parse errors for partial chunks
                }
            }
        }
    }
    console.log('\n');
}

chatRag('What were the key action items from the last meeting?');
