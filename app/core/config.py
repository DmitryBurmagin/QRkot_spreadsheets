from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    title: str = 'QRKot'
    description: str = 'Благотворительный проект, сбор средств для котиков.'
    database_url: str = 'sqlite+aiosqlite:///./qrkot.db'
    debug: bool = True
    secret_key: str = 'SECRET'

    type: Optional[str]
    project_id: Optional[str]
    private_key_id: Optional[str]
    private_key: Optional[str]
    client_email: Optional[str]
    client_id: Optional[str]
    auth_uri: Optional[str]
    token_uri: Optional[str]
    auth_provider_x509_cert_url: Optional[str]
    client_x509_cert_url: Optional[str]
    email: Optional[str]

    class Config:
        env_file = '.env'


settings = Settings()
