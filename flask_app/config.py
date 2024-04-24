import os
import dotenv

dotenv.load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
MONGODB_HOST = os.getenv('MONGODB_HOST')