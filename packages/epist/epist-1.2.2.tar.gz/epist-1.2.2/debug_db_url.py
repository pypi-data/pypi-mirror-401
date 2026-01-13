# from src.core.config import settings


def test_db_url_generation():
    print("Testing DB URL Generation logic...")

    # Simulate env vars
    mock_values = {
        "DB_USER": "epist_user",
        "DB_PASSWORD": "epist-db-password-staging:latest",  # This is a secret reference, but in Cloud Run it's the actual password
        "DB_HOST": "/cloudsql/audiointelligence-3cb34:us-central1:epist-db-staging",
        "DB_NAME": "epist",
    }

    # We need to mock ValidationInfo but since it's hard to instantiate,
    # let's just inspect the logic we extracted

    db_host = mock_values["DB_HOST"]
    db_password = mock_values["DB_PASSWORD"]
    db_user = mock_values["DB_USER"]
    db_name = mock_values["DB_NAME"]

    if db_host.startswith("/"):
        from urllib.parse import quote_plus

        password = quote_plus(db_password)
        user = quote_plus(db_user)
        # The issue might be here. asyncpg with storage socket expects host to be the directory
        # The 'host' param in query string is correct for storage
        url = f"postgresql+asyncpg://{user}:{password}@/{db_name}?host={db_host}"
        print(f"Generated URL: {url}")


test_db_url_generation()
