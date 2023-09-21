import os
from dotenv import load_dotenv


load_dotenv()
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DBNAME = os.getenv('DBNAME')
# DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'
USER='postgres'
PASSWORD='fantasy27'
HOST='localhost'
PORT='5432'
DBNAME='TechnicalTask'
DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'
