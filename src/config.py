from pathlib import Path
from dotenv import load_dotenv

# Get project root relative to this config file
PROJECT_ROOT = Path(__file__).parent.parent
print("Project root:", PROJECT_ROOT)

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
FINAL_DIR = DATA_DIR / "final"

# Load .env from project root
load_dotenv(PROJECT_ROOT / ".env")
