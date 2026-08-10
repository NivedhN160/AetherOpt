from aetheropt.db.base import Base
from aetheropt.db.session import engine
import aetheropt.db.models  # Ensures models are imported and attached to Base

def main():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

if __name__ == "__main__":
    main()
