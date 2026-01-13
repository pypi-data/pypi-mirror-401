import os
import sys

sys.path.append(os.path.join(os.getcwd(), "src"))
# Mock env vars
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["API_KEY"] = "test"
os.environ["SECRET_KEY"] = "test"

try:
    print("Import successful")
except Exception as e:
    print(f"Import failed: {e}")
    import traceback

    traceback.print_exc()
