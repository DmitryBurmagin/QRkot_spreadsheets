from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from app.core.config import settings

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

CREDS = ServiceAccountCreds(
    scopes=SCOPES,
    client_email=settings.google_api_client_email,
    private_key=settings.google_api_private_key,
    token_uri=settings.google_api_token_uri
)


async def get_google_client():
    async with Aiogoogle(service_account_creds=CREDS) as google:
        return google
