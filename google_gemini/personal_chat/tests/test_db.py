from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/rag_chat"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    print("Database connected successfully!")
