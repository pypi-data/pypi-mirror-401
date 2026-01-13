import {
    ICredentialType,
    INodeProperties,
} from 'n8n-workflow';

export class EpistApi implements ICredentialType {
    name = 'epistApi';
    displayName = 'Epist API';
    documentationUrl = 'https://docs.epist.ai/integrations';
    authenticate = {
        type: 'generic',
        properties: {
            headers: {
                'x-api-key': '={{$credentials.apiKey}}',
            },
        },
    } as const;
    properties: INodeProperties[] = [
        {
            displayName: 'API Key',
            name: 'apiKey',
            type: 'string',
            typeOptions: {
                password: true,
            },
            default: '',
        },
    ];
}
