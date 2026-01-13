import logging
from typing import BinaryIO

import google.auth
import google.auth.credentials
import requests
from google.auth.transport.requests import Request as AuthRequest

from core.config import settings

# Version: Fixed StorageService download_blob (2024-11-30)
logger = logging.getLogger(__name__)


class IAMSigningCredentials(google.auth.credentials.Credentials, google.auth.credentials.Signing):
    """
    Helper class to support V4 signing on Cloud Run by using the IAM Signer.
    Cloud Run service accounts usually don't have a private key for local signing.
    """

    def __init__(self, underlying_creds, service_account_email):
        # Set attributes before super().__init__ to be safe with any magic
        self.underlying_creds = underlying_creds
        self.service_account_email = service_account_email
        self._request = AuthRequest()

        # Lazy import for IAM signer to keep startup fast
        import google.auth.iam

        # IMPORTANT: The signer property is required by google-auth for V4 signing.
        # We must provide a concrete implementation of the abstract signer method.
        self._signer = google.auth.iam.Signer(self._request, self.underlying_creds, self.service_account_email)
        super().__init__()

    @property
    def signer(self):
        """Standard property expected by Signing base class."""
        return self._signer

    def refresh(self, request):
        self.underlying_creds.refresh(request)

    @property
    def token(self):
        return self.underlying_creds.token

    @token.setter
    def token(self, value):
        # Robust setter to handle both attribute and property assignments
        if hasattr(self.underlying_creds, "token"):
            try:
                self.underlying_creds.token = value
            except AttributeError:
                # Handle cases where token might be a read-only property on underlying creds
                pass

    @property
    def valid(self):
        return self.underlying_creds.valid

    @valid.setter
    def valid(self, value):
        if hasattr(self.underlying_creds, "valid"):
            try:
                self.underlying_creds.valid = value
            except AttributeError:
                pass

    @property
    def expiry(self):
        return getattr(self.underlying_creds, "expiry", None)

    @expiry.setter
    def expiry(self, value):
        if hasattr(self.underlying_creds, "expiry"):
            try:
                self.underlying_creds.expiry = value
            except AttributeError:
                pass

    @property
    def signer_email(self):
        return self.service_account_email

    def sign_bytes(self, message):
        return self._signer.sign(message)


class StorageService:
    def __init__(self):
        self.bucket_name = settings.GCS_BUCKET_NAME
        self.credentials = None
        self.project = None

    def _ensure_credentials(self):
        if not self.credentials:
            self.credentials, self.project = google.auth.default()

    def upload_file(self, file_obj: BinaryIO, destination_blob_name: str, content_type: str) -> str:
        """
        Uploads a file-like object to the bucket using GCS JSON API (HTTP) to bypass gRPC issues.
        """
        try:
            self._ensure_credentials()
            # Refresh credentials to get a valid token
            if not self.credentials.valid:
                self.credentials.refresh(AuthRequest())

            token = self.credentials.token

            url = f"https://storage.googleapis.com/upload/storage/v1/b/{self.bucket_name}/o?uploadType=media&name={destination_blob_name}"

            headers = {"Authorization": f"Bearer {token}", "Content-Type": content_type}

            # Ensure we are at the start of the file
            file_obj.seek(0)

            # Using data=file_obj allows requests to stream the upload if it's a file-like object
            logger.info(f"Uploading to GCS via HTTP: {url}")
            response = requests.post(url, headers=headers, data=file_obj)

            if response.status_code != 200:
                raise Exception(f"GCS Upload Failed: {response.status_code} - {response.text}")

            logger.info(f"File uploaded to {destination_blob_name}.")
            return f"gs://{self.bucket_name}/{destination_blob_name}"
        except Exception as e:
            import sys

            sys.stderr.write(f"ERROR: Failed to upload file to GCS: {e}\n")
            logger.error(f"Failed to upload file to GCS: {e}")
            raise e

    def download_blob(self, bucket_name: str, blob_name: str, destination_path: str):
        """
        Downloads a blob from GCS using HTTP to bypass gRPC issues.
        """
        try:
            self._ensure_credentials()
            # Refresh credentials to get a valid token
            if not self.credentials.valid:
                self.credentials.refresh(AuthRequest())

            token = self.credentials.token

            # URL format: https://storage.googleapis.com/storage/v1/b/{bucket}/o/{object}?alt=media
            # Need to URL-encode the object name
            from urllib.parse import quote

            encoded_blob_name = quote(blob_name, safe="")
            url = f"https://storage.googleapis.com/storage/v1/b/{bucket_name}/o/{encoded_blob_name}?alt=media"

            headers = {"Authorization": f"Bearer {token}"}

            logger.info(f"Downloading from GCS via HTTP: {url}")
            response = requests.get(url, headers=headers, stream=True)

            if response.status_code != 200:
                raise Exception(f"GCS Download Failed: {response.status_code} - {response.text}")

            # Write to file
            with open(destination_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            logger.info(f"File downloaded to {destination_path}.")
        except Exception as e:
            logger.error(f"Failed to download file from GCS: {e}")
            raise e

    def get_file_stream(self, bucket_name: str, blob_name: str):
        """
        Returns a generator for the file content and its content type.
        """
        try:
            self._ensure_credentials()
            # Refresh credentials to get a valid token
            if not self.credentials.valid:
                self.credentials.refresh(AuthRequest())

            token = self.credentials.token

            # URL format: https://storage.googleapis.com/storage/v1/b/{bucket}/o/{object}?alt=media
            from urllib.parse import quote

            encoded_blob_name = quote(blob_name, safe="")
            url = f"https://storage.googleapis.com/storage/v1/b/{bucket_name}/o/{encoded_blob_name}?alt=media"

            headers = {"Authorization": f"Bearer {token}"}

            logger.info(f"Streaming from GCS via HTTP: {url}")
            response = requests.get(url, headers=headers, stream=True)

            if response.status_code != 200:
                raise Exception(f"GCS Download Failed: {response.status_code} - {response.text}")

            return response.iter_content(chunk_size=8192), response.headers.get(
                "Content-Type", "application/octet-stream"
            )
        except Exception as e:
            logger.error(f"Failed to stream file from GCS: {e}")
            raise e

    def upload_from_url(self, url: str, destination_blob_name: str, content_type: str = "audio/mpeg") -> str:
        """
        Downloads from a public URL and uploads to GCS using stream transfer.
        Uses requests for both download and upload to keep dependencies simple and synchronous for now (or thread-pooled).
        """
        try:
            self._ensure_credentials()
            if not self.credentials.valid:
                self.credentials.refresh(AuthRequest())

            token = self.credentials.token
            upload_url = f"https://storage.googleapis.com/upload/storage/v1/b/{self.bucket_name}/o?uploadType=media&name={destination_blob_name}"
            headers = {"Authorization": f"Bearer {token}", "Content-Type": content_type}

            logger.info(f"Stream-uploading from {url} to GCS {destination_blob_name}...")

            # Stream download
            with requests.get(url, stream=True, allow_redirects=True, timeout=60) as r:
                r.raise_for_status()

                # Stream upload
                # requests.post supports passing a generator/iterable as data
                response = requests.post(upload_url, headers=headers, data=r.iter_content(chunk_size=8192))

            if response.status_code != 200:
                raise Exception(f"GCS Stream Upload Failed: {response.status_code} - {response.text}")

            gcs_uri = f"gs://{self.bucket_name}/{destination_blob_name}"
            logger.info(f"Successfully bridged file to {gcs_uri}")
            return gcs_uri

        except Exception as e:
            logger.error(f"Failed to bridge file to GCS: {e}")
            raise e

    def delete_file(self, bucket_name: str, blob_name: str):
        """
        Deletes a blob from GCS using HTTP.
        """
        try:
            self._ensure_credentials()
            if not self.credentials.valid:
                self.credentials.refresh(AuthRequest())

            token = self.credentials.token

            # URL encode blob name
            from urllib.parse import quote

            encoded_blob_name = quote(blob_name, safe="")

            url = f"https://storage.googleapis.com/storage/v1/b/{bucket_name}/o/{encoded_blob_name}"

            headers = {"Authorization": f"Bearer {token}"}

            logger.info(f"Deleting GCS blob via HTTP: {url}")
            response = requests.delete(url, headers=headers)

            if response.status_code not in [204, 200]:
                # 404 is fine, it's already gone
                if response.status_code == 404:
                    logger.warning(f"File {blob_name} not found in bucket {bucket_name}, assuming deleted.")
                    return
                raise Exception(f"GCS Delete Failed: {response.status_code} - {response.text}")

            logger.info(f"File {blob_name} deleted from {bucket_name}.")

        except Exception as e:
            logger.error(f"Failed to delete file from GCS: {e}")
            raise e

    def generate_signed_url(self, bucket_name: str, blob_name: str, expiration_minutes: int = 15) -> str:
        """
        Generates a V4 signed URL for the blob.
        Uses lazy import of google-cloud-storage to avoid gRPC/startup issues.
        Handles Cloud Run credentials (no private key) by using IAM Signer.
        """
        try:
            self._ensure_credentials()

            # Ensure credentials are valid/refreshed
            if not self.credentials.valid:
                from google.auth.transport.requests import Request as AuthRequest

                self.credentials.refresh(AuthRequest())

            creds = self.credentials

            # Check if credentials have signing capability (private key).
            # ComputeEngineCredentials (Cloud Run) usually don't.
            if not getattr(creds, "sign_bytes", None):
                sa_email = getattr(creds, "service_account_email", None)
                if sa_email:
                    # Resolve 'default' to actual email if possible, or assume Signer/GCS handles it.
                    # Note: For V4 signing, the email must be accurate in the URL.
                    # If 'default', we might need to fetch it, but usually standard credentials
                    # might resolve it after refresh or we rely on the signer.
                    # Let's wrap it.

                    logger.info(f"Using IAM Signing for Signed URL (Email: {sa_email})")
                    creds = IAMSigningCredentials(creds, sa_email)

            # Lazy import to keep the class lightweight and safe from gRPC hangs
            from datetime import timedelta

            from google.cloud import storage

            # Initialize client with (potentially wrapped) credentials
            client = storage.Client(credentials=creds, project=self.project)
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(blob_name)

            url = blob.generate_signed_url(version="v4", expiration=timedelta(minutes=expiration_minutes), method="GET")

            logger.info(f"Generated signed URL for {blob_name}")
            return url

        except Exception as e:
            logger.error(f"Failed to generate signed URL: {e}")
            raise e
