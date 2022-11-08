import os

root_path = os.environ.get('API_ROOT_PATH', '')
db_url = os.environ.get('API_DB_URL', 'mongodb://root:example@localhost:27017/')
db_name = os.environ.get('API_DB_NAME', 'auth_service')
