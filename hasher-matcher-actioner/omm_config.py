import os
from threatexchange.signal_type.pdq.signal import PdqSignal
from threatexchange.signal_type.md5 import VideoMD5Signal

PRODUCTION = os.environ.get("PRODUCTION", "false") == "true"
DBUSER = os.environ.get("POSTGRES_USER", "media_match")
DBPASS = os.environ.get("POSTGRES_PASSWORD", "hunter2")
DBHOST = os.environ.get("POSTGRES_HOST", "db")
DBNAME = os.environ.get("POSTGRES_DBNAME", "media_match")
DATABASE_URI = f"postgresql+psycopg2://{DBUSER}:{DBPASS}@{DBHOST}/{DBNAME}"

# Role configuration
ROLE_HASHER = os.environ.get("ROLE_HASHER", "false") == "true"
ROLE_MATCHER = os.environ.get("ROLE_MATCHER", "false") == "true"
ROLE_CURATOR = os.environ.get("ROLE_CURATOR", "false") == "true"

# Installed SignalTypes
SIGNAL_TYPES = [PdqSignal, VideoMD5Signal]

# Background tasks
TASK_INDEX_CACHE = os.environ.get("TASK_INDEX_CACHE", "false") == "true"
TASK_INDEXER = os.environ.get("TASK_INDEXER", "false") == "true"
TASK_FETCHER = os.environ.get("TASK_FETCHER", "false") == "true"
