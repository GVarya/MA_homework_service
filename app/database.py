# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, Session

# from app.settings import settings
# from app.schemas.base_schema import Base

# DATABASE_URL = settings.postgres_url

# engine = create_engine(
#     DATABASE_URL,
#     echo=False,         
#     future=True,
# )

# SessionLocal = sessionmaker(
#     bind=engine,
#     autocommit=False,
#     autoflush=False,
# )

# def init_db() -> None:
   
#     Base.metadata.create_all(bind=engine)

# def get_db() -> Session: # type: ignore
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
# app/database.py
# app/database.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

from app.settings import settings

# Используем URL из настроек без дополнительной обработки
DATABASE_URL = settings.postgres_url

print(f"Final database URL: {DATABASE_URL}")

# Создаем engine с минимальными настройками
engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    pool_pre_ping=True,
    pool_recycle=300,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# Простая функция тестирования подключения
def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            db_version = result.fetchone()[0]
            print(f"✅ Connected to PostgreSQL: {db_version}")
            return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def init_db():
    """Создаем таблицы если их нет"""
    from app.schemas.base_schema import Base
    
    # Импортируем все модели чтобы они зарегистрировались
    import app.schemas.homework
    import app.schemas.solution
    import app.schemas.proggress
    
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created/verified")
        
        # Проверим, какие таблицы существуют
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = result.fetchall()
            print(f"Tables in database: {[t[0] for t in tables]}")
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()