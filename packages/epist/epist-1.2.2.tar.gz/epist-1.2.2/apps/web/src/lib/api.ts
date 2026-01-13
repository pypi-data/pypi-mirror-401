import axios, { AxiosError } from 'axios';
import { auth } from './firebase';
import { Organization, OrganizationInvitation } from './types/user';

const API_URL = process.env.NEXT_PUBLIC_API_URL;
const API_KEY = process.env.NEXT_PUBLIC_API_KEY;

if (!API_URL) {
    console.warn('NEXT_PUBLIC_API_URL is not defined. API calls may fail.');
}

// Create axios instance
const apiClient = axios.create({
    baseURL: API_URL,
    timeout: 30000, // 30s timeout
});

// Configure defaults
if (API_KEY) {
    apiClient.defaults.headers.common['X-API-Key'] = API_KEY;
}

// Add auth interceptor
apiClient.interceptors.request.use(async (config) => {
    const user = auth.currentUser;
    if (user) {
        try {
            const token = await user.getIdToken();
            console.log('[API] Attaching Bearer token to request:', config.url);
            config.headers.Authorization = `Bearer ${token}`;
        } catch (error) {
            console.error('[API] Failed to get ID token:', error);
            // We proceed without token, or we could throw. 
            // If we don't throw, 401 will likely happen, which is fine.
        }
    } else {
        console.log('[API] No user found, request sent without Bearer token:', config.url);
    }

    // Inject API Key from localStorage if not already present
    if (!config.headers['X-API-Key']) {
        const storedKey = localStorage.getItem('last_generated_api_key');
        if (storedKey) {
            config.headers['X-API-Key'] = storedKey;
        }
    }

    return config;
});

// Response interceptor for global error handling
apiClient.interceptors.response.use(
    (response) => response,
    (error: AxiosError) => {
        if (error.response) {
            // Server responded with a status code outside 2xx
            console.error('API Error:', error.response.status, error.response.data);
        } else if (error.request) {
            // Request was made but no response received
            console.error('Network Error:', error.request);
        } else {
            // Something happened in setting up the request
            console.error('Request Error:', error.message);
        }
        return Promise.reject(error);
    }
);

export interface AudioStatus {
    id: string;
    status: 'pending' | 'processing' | 'completed' | 'failed';
    title: string;
    created_at: string;
    is_public?: boolean;
    meta_data?: Record<string, unknown>;
    transcript?: string;
    summary?: string;
    entities?: Record<string, unknown>[];
}

export interface TranscriptSegment {
    id: string;
    transcript_id: string;
    start: number;
    end: number;
    text: string;
    speaker?: string;
    confidence?: number;
    embedding?: number[];
}

export interface Transcript {
    id: string;
    audio_resource_id: string;
    language?: string;
    model?: string;
    text: string;
    created_at: string;
    segments: TranscriptSegment[];
}

export interface ChatMessage {
    role: 'user' | 'assistant' | 'system';
    content: string;
}

export interface Citation {
    id: string;
    text: string;
    start: number;
    end: number;
    score: number;
}

export interface ChatResponse {
    id: string;
    object: string;
    created: number;
    model: string;
    choices: {
        index: number;
        message: ChatMessage;
        finish_reason: string;
    }[];
    citations?: Citation[];
    trace_id?: string;
}

export interface SearchResult {
    id: string;
    text: string;
    start: number;
    end: number;
    score: number;
    methods: string[];
}

export interface SystemStats {
    audio_count: number;
    transcript_count: number;
    segment_count: number;
}

export interface TraceEvent {
    id: string;
    trace_id: string;
    span_id: string;
    parent_span_id?: string;
    event_type: string;
    component: string;
    name: string;
    inputs: Record<string, unknown>;
    outputs: Record<string, unknown>;
    meta: Record<string, unknown>;
    start_time: string;
    end_time: string;
    latency_ms: number;
    status: string;
    error_message?: string;
}

export interface ApiKey {
    id: string;
    name: string;
    prefix: string;
    created_at: string;
    last_used_at?: string;
    key?: string; // Only returned on creation
}

export interface HealthStatus {
    status: string;
    service: string;
}

export interface RequestLog {
    id: string;
    request_id: string;
    method: string;
    path: string;
    status_code: number;
    latency_ms: number;
    ip_address?: string;
    user_agent?: string;
    created_at: string;
}

export interface UserProfile {
    id: string;
    email: string;
    full_name?: string;
    is_superuser?: boolean;
    is_active?: boolean;
    onboarding_completed?: boolean;
    organization?: Organization;
}

export interface AdminStats {
    users: number;
    organizations: number;
    audio_resources: number;
    active_users_24h: number;
}

export interface AdminUsageMetric {
    date: string;
    requests: number;
    avg_latency_ms: number;
}

export interface AdminOrganization {
    id: string;
    name: string;
    tier: string;
    user_count: number;
    subscription_status: string;
    created_at: string;
}

export interface AdminUser {
    id: string;
    email: string;
    full_name: string;
    role: string;
    is_superuser: boolean;
    is_active: boolean;
    created_at: string;
    organization_id: string;
}

export interface AdminRequestLog {
    id: string;
    method: string;
    path: string;
    status_code: number;
    latency_ms: number;
    created_at: string;
    user_id: string;
}

export const api = {
    async listAudio(limit: number = 50, offset: number = 0): Promise<AudioStatus[]> {
        const response = await apiClient.get<AudioStatus[]>(`/audio`, {
            params: { limit, offset }
        });
        return response.data;
    },

    async uploadAudio(file: File): Promise<AudioStatus> {
        const formData = new FormData();
        formData.append('file', file);

        const response = await apiClient.post<AudioStatus>(`/audio/upload`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    async transcribeUrl(
        url: string,
        rag_enabled: boolean = true,
        language: string = 'en',
        preset: string = 'general',
        webhook_url?: string
    ): Promise<AudioStatus> {
        const response = await apiClient.post<AudioStatus>(`/audio/transcribe_url`, {
            audio_url: url,
            rag_enabled,
            language,
            preset,
            webhook_url
        });
        return response.data;
    },

    async getAudioStatus(id: string): Promise<AudioStatus> {
        const response = await apiClient.get<AudioStatus>(`/audio/${id}`);
        return response.data;
    },

    async updateAudio(id: string, data: { title?: string; is_public?: boolean }): Promise<AudioStatus> {
        const response = await apiClient.patch<AudioStatus>(`/audio/${id}`, data);
        return response.data;
    },

    async deleteAudio(id: string): Promise<void> {
        await apiClient.delete(`/audio/${id}`);
    },

    async getAudioContent(id: string): Promise<Blob> {
        const response = await apiClient.get(`/audio/${id}/content`, {
            responseType: 'blob'
        });
        return response.data;
    },

    async search(
        query: string,
        limit: number = 10,
        tier: 'free' | 'pro' = 'free',
        rrf_k?: number,
        rerank_model?: string
    ): Promise<SearchResult[]> {
        const response = await apiClient.post<SearchResult[]>(`/search`, {
            query,
            limit,
            tier,
            rrf_k,
            rerank_model,
        });
        return response.data;
    },

    async getStats(): Promise<SystemStats> {
        const response = await apiClient.get<SystemStats>(`/stats`);
        return response.data;
    },

    async getTranscript(audioId: string): Promise<Transcript> {
        const response = await apiClient.get<Transcript>(`/audio/${audioId}/transcript`);
        return response.data;
    },

    async chat(
        messages: ChatMessage[],
        stream: boolean = false,
        tier: string = 'free',
        rrf_k?: number,
        rerank_model?: string,
        audio_resource_id?: string,
        model: string = "gpt-3.5-turbo"
    ): Promise<ChatResponse | ReadableStream> {
        const payload = { messages, stream, tier, rrf_k, rerank_model, audio_resource_id, model };
        if (stream) {
            const response = await fetch(`${API_URL}/chat/completions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-API-Key': localStorage.getItem('last_generated_api_key') || '',
                    ...(auth.currentUser ? { 'Authorization': `Bearer ${await auth.currentUser.getIdToken()}` } : {})
                },
                body: JSON.stringify(payload),
            });
            if (!response.body) throw new Error('No response body');
            return response.body as ReadableStream;
        } else {
            const response = await apiClient.post<ChatResponse>('/chat/completions', payload);
            return response.data;
        }
    },

    async getLogs(
        limit: number = 50,
        offset: number = 0,
        status?: number,
        method?: string,
        startTime?: string,
        endTime?: string,
        requestId?: string
    ): Promise<RequestLog[]> {
        const response = await apiClient.get<RequestLog[]>(`/logs`, {
            params: {
                limit,
                offset,
                status_code: status,
                method,
                start_time: startTime,
                end_time: endTime,
                request_id: requestId
            }
        });
        return response.data;
    },

    // Auth & Keys
    async getMe(): Promise<UserProfile> {
        const response = await apiClient.get<UserProfile>(`/auth/me`);
        return response.data;
    },

    async completeOnboarding(orgName: string): Promise<void> {
        await apiClient.post(`/auth/onboarding`, { organization_name: orgName });
    },

    async getApiKeys(): Promise<ApiKey[]> {
        const response = await apiClient.get<ApiKey[]>(`/auth/api-keys`);
        return response.data;
    },

    // Organization & Team
    async getOrganization(): Promise<Organization> {
        const response = await apiClient.get<Organization>(`/organizations/me`);
        return response.data;
    },

    async getMembers(): Promise<AdminUser[]> {
        const response = await apiClient.get<AdminUser[]>(`/organizations/members`);
        return response.data;
    },

    async inviteMember(email: string, role: 'admin' | 'member' = 'member'): Promise<OrganizationInvitation> {
        const response = await apiClient.post<OrganizationInvitation>(`/organizations/invite`, { email, role });
        return response.data;
    },

    async getInvitations(): Promise<OrganizationInvitation[]> {
        const response = await apiClient.get<OrganizationInvitation[]>(`/organizations/invitations`);
        return response.data;
    },

    async removeMember(userId: string): Promise<void> {
        await apiClient.delete(`/organizations/members/${userId}`);
    },

    async createApiKey(name: string): Promise<ApiKey> {
        const response = await apiClient.post<ApiKey>(`/auth/api-keys`, null, {
            params: { name }
        });
        return response.data;
    },

    async revokeApiKey(keyId: string): Promise<void> {
        await apiClient.delete(`/auth/api-keys/${keyId}`);
    },

    async renameApiKey(keyId: string, name: string): Promise<ApiKey> {
        const response = await apiClient.put<ApiKey>(`/auth/api-keys/${keyId}`, null, {
            params: { name }
        });
        return response.data;
    },

    // System
    async getHealth(): Promise<HealthStatus> {
        // Health check is at root /health, not /api/v1/health usually, 
        // but let's check main.py. It is at /health.
        // API_URL is .../api/v1. So we need to go up.
        const baseUrl = API_URL?.replace('/api/v1', '');
        // Use axios directly here to avoid base URL issues or create a new instance
        const response = await axios.get<HealthStatus>(`${baseUrl}/health`);
        return response.data;
    },

    async getTraces(limit: number = 50, offset: number = 0, rootOnly: boolean = true): Promise<TraceEvent[]> {
        const response = await apiClient.get<TraceEvent[]>(`/traces`, {
            params: { limit, offset, root_only: rootOnly }
        });
        return response.data;
    },

    async getTraceDetails(traceId: string): Promise<TraceEvent[]> {
        const response = await apiClient.get<TraceEvent[]>(`/traces/${traceId}`);
        return response.data;
    },

    // Billing
    async createCheckoutSession(planId?: string): Promise<{ url: string }> {
        const response = await apiClient.post<{ url: string }>(`/billing/checkout`, null, {
            params: { plan_id: planId }
        });
        return response.data;
    },

    async createPortalSession(): Promise<{ url: string }> {
        const response = await apiClient.post<{ url: string }>(`/billing/portal`);
        return response.data;
    },

    // Admin
    async getAdminStats(): Promise<AdminStats> {
        return (await apiClient.get<AdminStats>(`/admin/stats`)).data;
    },
    async getAdminUsage(days: number = 7): Promise<AdminUsageMetric[]> {
        return (await apiClient.get<AdminUsageMetric[]>(`/admin/usage`, { params: { days } })).data;
    },
    async getAdminOrganizations(): Promise<AdminOrganization[]> {
        return (await apiClient.get<AdminOrganization[]>(`/admin/organizations`)).data;
    },
    async getAdminUsers(): Promise<AdminUser[]> {
        return (await apiClient.get<AdminUser[]>(`/admin/users`)).data;
    },
    async getAdminLogs(statusCode?: number): Promise<AdminRequestLog[]> {
        return (await apiClient.get<AdminRequestLog[]>(`/admin/logs`, { params: { status_code: statusCode } })).data;
    },
    async updateAdminUser(userId: string, data: { is_superuser?: boolean; is_active?: boolean }): Promise<AdminUser> {
        return (await apiClient.patch<AdminUser>(`/admin/users/${userId}`, data)).data;
    },
    async updateAdminOrganization(orgId: string, data: { tier?: string; subscription_status?: string }): Promise<AdminOrganization> {
        return (await apiClient.patch<AdminOrganization>(`/admin/organizations/${orgId}`, data)).data;
    },

    // Webhooks
    async createWebhook(url: string, events: string[], description?: string): Promise<Webhook> {
        return (await apiClient.post<Webhook>(`/integrations`, { url, events, description })).data;
    },

    async listWebhooks(): Promise<Webhook[]> {
        return (await apiClient.get<Webhook[]>(`/integrations`)).data;
    },

    async deleteWebhook(id: string): Promise<void> {
        await apiClient.delete(`/integrations/${id}`);
    }
};

export interface Webhook {
    id: string;
    url: string;
    events: string[];
    description?: string;
    created_at: string;
    is_active: boolean;
    secret?: string; // Only returned on creation
}
