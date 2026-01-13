import json

from google.cloud import tasks_v2

from core.config import settings


class QueueService:
    def __init__(self):
        try:
            self.client = tasks_v2.CloudTasksClient()
            self.queue_path = settings.CLOUD_TASKS_QUEUE_PATH
            self.service_account_email = settings.SERVICE_ACCOUNT_EMAIL
        except Exception as e:
            import sys

            sys.stderr.write(f"CRITICAL: Failed to initialize QueueService: {e}\n")
            raise e

    def enqueue_transcription(
        self,
        audio_id: str,
        audio_url: str,
        preset: str = "general",
        chunking_config: dict | None = None,
    ):
        """
        Enqueue a transcription task to Cloud Tasks.
        """
        # Construct the task payload
        payload = {
            "audio_id": str(audio_id),
            "audio_url": audio_url,
            "preset": preset,
            "chunking_config": chunking_config,
        }

        # Construct the task
        task = {
            "http_request": {
                "http_method": tasks_v2.HttpMethod.POST,
                "url": f"{settings.API_BASE_URL}/api/v1/tasks/process-audio",
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(payload).encode(),
                "oidc_token": {
                    "service_account_email": self.service_account_email,
                },
            }
        }

        # Create the task
        try:
            response = self.client.create_task(parent=self.queue_path, task=task)
            return response
        except Exception as e:
            import sys

            sys.stderr.write(f"ERROR: Failed to create Cloud Task: {e}\n")
            raise e
