import os
import sys

# Mock Env Vars
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"
os.environ["API_KEY"] = "test"
os.environ["SECRET_KEY"] = "test"
os.environ["OPENAI_API_KEY"] = "test"
os.environ["FIREWORKS_API_KEY"] = "test"
os.environ["GOOGLE_CLOUD_PROJECT"] = "test"

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

try:
    print("Importing app...")
    from src.main import app

    print("App imported successfully.")

    import uvicorn

    print("Starting uvicorn...")
    # Dry run
    config = uvicorn.Config(app, host="0.0.0.0", port=8080)
    server = uvicorn.Server(config)
    # We won't actually run it to block, just check instantiation
    print("Uvicorn server initialized.")
except Exception as e:
    print(f"Startup failed: {e}")
    import traceback

    traceback.print_exc()
