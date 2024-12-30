from models import Base
from config.config import engine

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Таблиці створено успішно!")
