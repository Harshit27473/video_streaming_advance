from secret_keys import SecretKeys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


secret_keys = SecretKeys()

engine =create_engine(secret_keys.POSTGRES_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close()