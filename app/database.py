from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import psycopg2
import time
from .config import settings


password = quote_plus(settings.database_password)
# Corrected connection string
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:

#     try: 
#         connection = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='485@Sql$499', port=5433)
#         cursor = connection.cursor()
#         print('Connected to the database')
#         break

#     except Exception as e:
#         print("Connecting to the database failed")
#         print(f"Error: {e}")
#         time.sleep(5)