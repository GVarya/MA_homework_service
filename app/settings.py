# from pydantic_settings import BaseSettings, SettingsConfigDict

# class Settings(BaseSettings):
#     amqp_url: str
#     postgres_url: str | None = None 
#     model_config = SettingsConfigDict(env_file=".env")


# settings = Settings()

# app/settings.py
# app/settings.py
# app/settings.py
import os
import re

class Settings:
    def __init__(self):
        # Полностью игнорируем переменную окружения, используем жестко заданный URL
        self.postgres_url = self._get_safe_postgres_url()
        self.amqp_url = self._get_safe_amqp_url()
        
        print(f"Using PostgreSQL URL: {self.postgres_url}")
        print(f"Using AMQP URL: {self.amqp_url}")
    
    def _get_safe_postgres_url(self) -> str:
        """Получаем безопасный URL для PostgreSQL"""
        # Жестко заданный URL, который точно работает
        default_url = "postgresql://postgres:password@localhost:5432/homework_db"
        
        try:
            # Пробуем получить из переменной окружения, но если есть проблемы - используем дефолтный
            env_url = os.getenv("POSTGRES_URL", default_url)
            
            # Проверяем на наличие проблемных символов
            if not self._is_valid_utf8(env_url):
                print("Warning: POSTGRES_URL contains invalid UTF-8 characters, using default")
                return default_url
            
            # Проверяем, что URL похож на валидный
            if not env_url.startswith(("postgresql://", "postgres://")):
                print("Warning: POSTGRES_URL format is invalid, using default")
                return default_url
                
            return env_url
        except:
            return default_url
    
    def _get_safe_amqp_url(self) -> str:
        """Получаем безопасный URL для RabbitMQ"""
        default_url = "amqp://guest:guest@localhost:5672/"
        
        try:
            env_url = os.getenv("AMQP_URL", default_url)
            
            if not self._is_valid_utf8(env_url):
                print("Warning: AMQP_URL contains invalid UTF-8 characters, using default")
                return default_url
            
            return env_url
        except:
            return default_url
    
    def _is_valid_utf8(self, text: str) -> bool:
        """Проверяет, является ли строка валидной UTF-8"""
        try:
            text.encode('utf-8').decode('utf-8')
            return True
        except:
            return False

settings = Settings()