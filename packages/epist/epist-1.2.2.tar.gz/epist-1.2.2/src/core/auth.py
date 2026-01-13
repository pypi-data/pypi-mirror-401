import logging

import firebase_admin
from fastapi import HTTPException, status
from firebase_admin import auth

logger = logging.getLogger(__name__)

import os

# Initialize Firebase Admin
# In Cloud Run, it uses Application Default Credentials automatically.
# Locally, it expects GOOGLE_APPLICATION_CREDENTIALS env var or no args if using gcloud auth application-default login.
try:
    firebase_admin.get_app()
except ValueError:
    firebase_project_id = os.getenv("FIREBASE_PROJECT_ID")
    if firebase_project_id:
        logger.info(f"Initializing Firebase Admin with project ID: {firebase_project_id}")
        firebase_admin.initialize_app(options={"projectId": firebase_project_id})
    else:
        firebase_admin.initialize_app()


def verify_firebase_token(token: str) -> dict:
    """
    Verifies the Firebase ID token and returns the decoded token.
    Raises HTTPException if invalid.
    """
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        logger.error(f"Firebase token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
