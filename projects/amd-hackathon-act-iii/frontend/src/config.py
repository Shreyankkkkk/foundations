"""All constants in one place: paths, data keys, the endpoint variable name."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent   # frontend/
DATA_DIR = ROOT / "data"
KEYS = ["sop", "notes", "flags", "benchmark", "amd"]
API_URL_ENV = "DRIFT_API_URL"                   # environment variable, never commit its value
API_TIMEOUT_S = 3
CACHE_TTL_S = 30
