from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
load_dotenv()


API_KEY = os.getenv("API_KEY")

def postgres_conn():
  db_user = os.getenv("DB_USER")
  db_password = os.getenv("DB_PASSWORD")
  db_host = os.getenv("DB_HOST")
  db_port = os.getenv("DB_PORT")
  db_name = os.getenv("DB_NAME")

  db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

  try:
    engine = create_engine(db_url, future=True)
    with engine.connect() as connection:
      connection.execute(text("SELECT 1")) # testa se a conexão está ativa
    return engine
  except Exception as e:
    print(e)
    return None 
