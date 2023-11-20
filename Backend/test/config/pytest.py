import os

from dotenv import load_dotenv

load_dotenv()
SKIP_TEST = os.getenv("TEST_STAGE", default="local") == "ci"
