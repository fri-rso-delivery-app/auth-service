import os

root_path = os.environ.get('API_ROOT_PATH', '')
http_port = int(os.environ.get('API_HTTP_PORT', '8001'))
db_url = os.environ.get('API_DB_URL', 'mongodb://root:example@localhost:27017/')
db_name = os.environ.get('API_DB_NAME', 'auth_service')

# to get a viable secret run:
# openssl rand -hex 32
secret_key = os.environ.get('API_SECRET_KEY', 'SECRET_REPLACE_ME')
jwt_token_expire_minutes = int(os.environ.get('API_TOKEN_EXPIRE_MIN', '60'))
