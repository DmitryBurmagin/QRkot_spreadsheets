from pydantic import BaseSettings


class Settings(BaseSettings):
    title: str = 'QRKot'
    description: str = 'Благотворительный проект, сбор средств для котиков.'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    debug: bool = True
    secret_key: str = 'SECRET'
    google_api_client_email: str
    google_api_private_key: str
    google_api_token_uri: str
    email: str

    class Config:
        env_file = '.env'


settings = Settings()
