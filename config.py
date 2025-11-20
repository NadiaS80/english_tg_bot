# config.py

login = 'YOUR-LOGIN'
password = 'YOUR-PASSWORD'
host = 'YOUR-HOST'
port = 'YOUR-PORT'
db_name = 'YOUR_DATA_BASE_NAME'

DB_DSN = f'postgresql://{login}:{password}@{host}:{port}/{db_name}'

TG_BOT_TOKEN = 'YOUR-TOKEN'

HF_API_URL = 'https://router.huggingface.co/v1/chat/completions'
HUGGING_FACE_TOKEN = 'YOUR-TOKEN'
HF_MODEL_NAME = 'deepseek-ai/DeepSeek-V3-0324'