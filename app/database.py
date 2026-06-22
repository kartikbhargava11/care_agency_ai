# this file allows data to flow from application to database and vice-versa

from sqlalchemy import create_engine # imports the tool that opens the actual physical connection file
from sqlalchemy.orm import declarative_base, sessionmaker # blueprint tools
from config.settings import settings


# opens up the database file
# [CRITICAL] check_same_thread=False allows FastAPI's async loop to read and write to the same
# database file concurrently without throwing lock errors
engine = create_engine(
    settings.DATABASE_URL, connect_args={'check_same_thread':False}
)

# [CRITICAL]
# telling SQLalchemy don't write anything to the database until we explicitly says db.commit()
# prevents half-written data from saving
# it also isolates database connections (i.e. sessions)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # initializes the structural base blueprint, every table model must inherit from this base class so SQLAlchemy knows it is a database table

# manages lifecycle of the database connection to prevent memory leaks
def get_db():
    db = SessionLocal() # opens a fresh database connection session for an incoming request

    try:
        yield db # hands the connection to API endpoint route so it can save the data
    finally:
        db.close() # clean-up. No matter API is successful or crashes.