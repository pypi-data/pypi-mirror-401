export type UserRole = 'admin' | 'member';

export interface Organization {
    id: string;
    name: string;
    tier: 'free' | 'starter' | 'pro' | 'enterprise';
    subscription_status: 'active' | 'trialing' | 'past_due' | 'canceled' | 'unpaid' | 'incomplete';
    current_period_end?: string;
    stripe_customer_id?: string;
    monthly_audio_seconds?: number;
    usage_reset_at?: string;
}

export interface User {
    id: string;
    email: string;
    full_name: string;
    avatar_url?: string;
    organization_id: string;
    role: UserRole;
    organization?: Organization;
}

export interface OrganizationInvitation {
    id: string;
    email: string;
    role: UserRole;
    status: 'pending' | 'accepted' | 'expired';
    created_at: string;
    expires_at: string;
}

export interface UsageStats {
    transcriptions_used: number;
    transcriptions_limit: number;
    searches_used: number;
    searches_limit: number;
}
