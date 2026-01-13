import axios, { AxiosInstance, AxiosError } from 'axios';

export interface EpistConfig {
    apiKey: string;
    baseUrl?: string;
}

export interface SearchResult {
    id: string;
    text: string;
    start: number;
    end: number;
    score: number;
    methods: string[];
}

export interface AudioStatus {
    id: string;
    status: 'pending' | 'processing' | 'completed' | 'failed';
    title: string;
    created_at: string;
    error?: string;
}

export interface TranscriptSegment {
    id: string;
    start: number;
    end: number;
    text: string;
    speaker?: string;
}

export interface Transcript {
    id: string;
    text: string;
    segments: TranscriptSegment[];
}

export class EpistError extends Error {
    constructor(message: string, public statusCode?: number, public originalError?: any) {
        super(message);
        this.name = 'EpistError';
    }
}

export class Epist {
    private client: AxiosInstance;

    constructor(config: EpistConfig) {
        this.client = axios.create({
            baseURL: config.baseUrl || 'https://epist-api-staging-920152096400.us-central1.run.app/api/v1',
            headers: {
                'X-API-Key': config.apiKey,
                // Do not set global Content-Type for all requests as it breaks multipart uploads
            },
        });
    }

    private handleError(error: unknown) {
        if (axios.isAxiosError(error)) {
            const message = error.response?.data?.detail || error.message;
            throw new EpistError(message, error.response?.status, error);
        }
        throw new EpistError(error instanceof Error ? error.message : 'Unknown error', undefined, error);
    }

    /**
     * Upload a local file.
     * @param file - File object (Browser) or fs.ReadStream (Node.js)
     */
    async uploadFile(file: any, preset: string = 'general'): Promise<AudioStatus> {
        try {
            // In Node 18+ and Browsers, FormData is global. 
            const formData = new FormData();
            formData.append('file', file);
            formData.append('preset', preset);

            const response = await this.client.post('/audio/upload', formData, {
                headers: {
                    // Axios will set 'Content-Type': 'multipart/form-data; boundary=...' automatically
                }
            });
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error; // unreachable
        }
    }

    /**
     * Transcribe audio from a URL
     */
    async transcribeUrl(
        url: string,
        ragEnabled: boolean = true,
        language: string = 'en',
        preset: string = 'general',
        chunkingConfig: any = null,
        webhookUrl?: string
    ): Promise<AudioStatus> {
        try {
            const payload: any = {
                audio_url: url,
                rag_enabled: ragEnabled,
                language,
                preset,
                chunking_config: chunkingConfig
            };
            if (webhookUrl) {
                payload.webhook_url = webhookUrl;
            }
            const response = await this.client.post('/audio/transcribe_url', payload);
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

    /**
     * Get status of an audio task
     */
    async getStatus(audioId: string): Promise<AudioStatus> {
        try {
            const response = await this.client.get(`/audio/${audioId}`);
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

    /**
     * Get full transcript
     */
    async getTranscript(audioId: string): Promise<Transcript> {
        try {
            const response = await this.client.get(`/audio/${audioId}/transcript`);
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

    /**
     * Search the knowledge base
     */
    async search(query: string, limit: number = 10, options?: Record<string, any>): Promise<SearchResult[]> {
        try {
            const payload = {
                query,
                limit,
                ...options
            };
            const response = await this.client.post('/search', payload);
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

    /**
     * Ingest a podcast RSS feed
     */
    async ingestRss(
        url: string,
        name?: string,
        refreshIntervalMinutes?: number,
        options?: {
            max_episodes?: number;
            start_date?: string;
            include_keywords?: string;
            exclude_keywords?: string;
        }
    ): Promise<any> {
        try {
            const payload: any = {
                url,
                name,
                refresh_interval_minutes: refreshIntervalMinutes,
                ...options
            };

            // Filter undefined values
            Object.keys(payload).forEach(key => payload[key] === undefined && delete payload[key]);

            const response = await this.client.post('/ingest/rss', payload);
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }
}

