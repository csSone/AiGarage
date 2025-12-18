import os

MODEL_PATH = os.environ.get('MODEL_PATH')
if MODEL_PATH is None:
    raise ValueError("MODEL_PATH environment variable is required")

PORT = int(os.environ.get('PORT', 8000))