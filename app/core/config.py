from pydantic import BaseSettings


class Settings(BaseSettings):
    title: str = 'QRKot'
    description: str = 'Благотворительный проект, сбор средств для котиков.'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    debug: bool = True
    secret_key: str = 'SECRET'

    type: str = 'service_account'
    client_email: str
    private_key: str
    token_uri: str
    project_id: str
    private_key_id: str
    client_id: str
    auth_uri: str = 'https://accounts.google.com/o/oauth2/auth'
    token_uri: str = 'https://oauth2.googleapis.com/token'
    auth_provider_x509_cert_url: str = (
        'https://www.googleapis.com/oauth2/v1/certs'
    )
    client_x509_cert_url: str
    email: str

    class Config:
        env_file = '.env'


settings = Settings()
