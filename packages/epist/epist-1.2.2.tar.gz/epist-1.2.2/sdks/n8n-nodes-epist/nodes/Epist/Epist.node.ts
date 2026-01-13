import {
    IDataObject,
    IExecuteFunctions,
    INodeExecutionData,
    INodeType,
    INodeTypeDescription,
} from 'n8n-workflow';

export class Epist implements INodeType {
    description: INodeTypeDescription = {
        displayName: 'Epist.ai',
        name: 'epist',
        icon: 'file:epist.svg',
        group: ['transform'],
        version: 1,
        subtitle: '={{$parameter["resource"] + ": " + $parameter["operation"]}}',
        description: 'Interact with Epist.ai Audio RAG Platform',
        defaults: {
            name: 'Epist.ai',
        },
        inputs: ['main'],
        outputs: ['main'],
        credentials: [
            {
                name: 'epistApi',
                required: true,
            },
        ],
        properties: [
            {
                displayName: 'Resource',
                name: 'resource',
                type: 'options',
                noDataExpression: true,
                options: [
                    {
                        name: 'Audio',
                        value: 'audio',
                    },
                    {
                        name: 'Search',
                        value: 'search',
                    },
                ],
                default: 'audio',
            },
            {
                displayName: 'Operation',
                name: 'operation',
                type: 'options',
                noDataExpression: true,
                displayOptions: {
                    show: {
                        resource: [
                            'audio',
                        ],
                    },
                },
                options: [
                    {
                        name: 'Transcribe URL',
                        value: 'transcribe_url',
                        description: 'Transcribe audio from a URL',
                        action: 'Transcribe audio from a URL',
                    },
                    {
                        name: 'Get Status',
                        value: 'get_status',
                        description: 'Get status of an audio resource',
                        action: 'Get an audio resource',
                    },
                    {
                        name: 'Upload',
                        value: 'upload',
                        description: 'Upload an audio file',
                        action: 'Upload an audio file',
                    },
                    {
                        name: 'Delete',
                        value: 'delete',
                        description: 'Delete an audio resource',
                        action: 'Delete an audio resource',
                    },
                ],
                default: 'transcribe_url',
            },
            {
                displayName: 'Operation',
                name: 'operation',
                type: 'options',
                noDataExpression: true,
                displayOptions: {
                    show: {
                        resource: [
                            'search',
                        ],
                    },
                },
                options: [
                    {
                        name: 'Query',
                        value: 'query',
                        description: 'Search your audio knowledge base',
                        action: 'Search audio knowledge base',
                    },
                ],
                default: 'query',
            },

            // ----------------------------------
            //         Audio: Transcribe URL
            // ----------------------------------
            {
                displayName: 'Audio URL',
                name: 'audioUrl',
                type: 'string',
                required: true,
                displayOptions: {
                    show: {
                        operation: [
                            'transcribe_url',
                        ],
                        resource: [
                            'audio',
                        ],
                    },
                },
                default: '',
                placeholder: 'https://example.com/audio.mp3',
            },
            {
                displayName: 'RAG Enabled',
                name: 'ragEnabled',
                type: 'boolean',
                default: true,
                displayOptions: {
                    show: {
                        operation: [
                            'transcribe_url',
                        ],
                        resource: [
                            'audio',
                        ],
                    },
                },
            },

            // ----------------------------------
            //         Audio: Upload
            // ----------------------------------
            {
                displayName: 'Binary Property',
                name: 'binaryPropertyName',
                type: 'string',
                default: 'data',
                required: true,
                displayOptions: {
                    show: {
                        operation: [
                            'upload',
                        ],
                        resource: [
                            'audio',
                        ],
                    },
                },
                description: 'Name of the binary property which contains the file to be uploaded',
            },
            {
                displayName: 'Preset',
                name: 'preset',
                type: 'options',
                options: [
                    {
                        name: 'General',
                        value: 'general',
                    },
                    {
                        name: 'Legal',
                        value: 'legal',
                    },
                    {
                        name: 'Medical',
                        value: 'medical',
                    },
                ],
                default: 'general',
                displayOptions: {
                    show: {
                        operation: [
                            'upload',
                        ],
                        resource: [
                            'audio',
                        ],
                    },
                },
            },

            // ----------------------------------
            //         Audio: Get Status / Delete
            // ----------------------------------
            {
                displayName: 'Audio ID',
                name: 'audioId',
                type: 'string',
                required: true,
                displayOptions: {
                    show: {
                        operation: [
                            'get_status',
                            'delete'
                        ],
                        resource: [
                            'audio',
                        ],
                    },
                },
                default: '',
            },

            // ----------------------------------
            //         Search: Query
            // ----------------------------------
            {
                displayName: 'Search Query',
                name: 'query',
                type: 'string',
                required: true,
                displayOptions: {
                    show: {
                        operation: [
                            'query',
                        ],
                        resource: [
                            'search',
                        ],
                    },
                },
                default: '',
            },
        ],
    };

    async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
        const items = this.getInputData();
        const returnData: INodeExecutionData[] = [];
        const resource = this.getNodeParameter('resource', 0) as string;
        const operation = this.getNodeParameter('operation', 0) as string;

        let responseData;

        for (let i = 0; i < items.length; i++) {
            try {
                if (resource === 'audio') {
                    if (operation === 'transcribe_url') {
                        const audio_url = this.getNodeParameter('audioUrl', i) as string;
                        const rag_enabled = this.getNodeParameter('ragEnabled', i) as boolean;

                        const body: IDataObject = {
                            audio_url,
                            rag_enabled,
                        };

                        responseData = await this.helpers.requestWithAuthentication.call(this, 'epistApi', {
                            method: 'POST',
                            uri: `https://api.epist.ai/api/v1/audio/transcribe_url`,
                            body,
                            json: true,
                        });
                    } else if (operation === 'get_status') {
                        const audio_id = this.getNodeParameter('audioId', i) as string;

                        responseData = await this.helpers.requestWithAuthentication.call(this, 'epistApi', {
                            method: 'GET',
                            uri: `https://api.epist.ai/api/v1/audio/${audio_id}`,
                            json: true,
                        });
                    } else if (operation === 'upload') {
                        const binaryPropertyName = this.getNodeParameter('binaryPropertyName', i) as string;
                        const preset = this.getNodeParameter('preset', i) as string;

                        if (items[i].binary && items[i].binary![binaryPropertyName]) {
                            const binaryData = items[i].binary![binaryPropertyName];
                            const fileContent = await this.helpers.getBinaryDataBuffer(i, binaryPropertyName);

                            const formData = {
                                file: {
                                    value: fileContent,
                                    options: {
                                        filename: binaryData.fileName,
                                        contentType: binaryData.mimeType,
                                    },
                                },
                                preset,
                            };

                            responseData = await this.helpers.requestWithAuthentication.call(this, 'epistApi', {
                                method: 'POST',
                                uri: `https://api.epist.ai/api/v1/audio/upload`,
                                formData,
                                json: true,
                            });
                        } else {
                            throw new Error(`Binary property "${binaryPropertyName}" not found on item.`);
                        }
                    } else if (operation === 'delete') {
                        const audio_id = this.getNodeParameter('audioId', i) as string;

                        responseData = await this.helpers.requestWithAuthentication.call(this, 'epistApi', {
                            method: 'DELETE',
                            uri: `https://api.epist.ai/api/v1/audio/${audio_id}`,
                            json: true,
                        });
                    }
                } else if (resource === 'search') {
                    if (operation === 'query') {
                        const query = this.getNodeParameter('query', i) as string;

                        const body: IDataObject = {
                            query,
                        };

                        responseData = await this.helpers.requestWithAuthentication.call(this, 'epistApi', {
                            method: 'POST',
                            uri: `https://api.epist.ai/api/v1/search/`,
                            body,
                            json: true,
                        });
                    }
                }

                if (Array.isArray(responseData)) {
                    returnData.push(...this.helpers.returnJsonArray(responseData as IDataObject[]));
                } else {
                    returnData.push({ json: responseData as IDataObject });
                }

            } catch (error) {
                if (this.continueOnFail()) {
                    returnData.push({ json: { error: (error as any).message } });
                    continue;
                }
                throw error;
            }
        }

        return [returnData];
    }
}
