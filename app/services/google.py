from datetime import datetime
from string import ascii_uppercase

from aiogoogle import Aiogoogle

from .constants import (DISCOVER_DRIVE_V3, DISCOVER_SHEETS_V4, FORMAT,
                        PERMISSIONS_CONFIG, SPREADSHEET_PROPERTIES,
                        TABLE_HEADER)


async def create_spreadsheet(wrapp_service: Aiogoogle):
    service = await wrapp_service.discover(*DISCOVER_SHEETS_V4)
    response = await wrapp_service.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_PROPERTIES)
    )
    return response['spreadsheetId']


async def set_user_permissions(
    wrapp_service: Aiogoogle,
    spreadsheet_id: str,
) -> None:
    service = await wrapp_service.discover(*DISCOVER_DRIVE_V3)
    await wrapp_service.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=PERMISSIONS_CONFIG
        ),
    )


async def spreadsheet_update_values(
    spreadsheet_id: str,
    projects: list,
    wrapp_service: Aiogoogle,
) -> None:
    service = await wrapp_service.discover(*DISCOVER_SHEETS_V4)
    table_values = TABLE_HEADER.copy()
    table_values[0].append(datetime.now().strftime(FORMAT))

    for project in projects:
        table_values.append([*project.values()])

    column = ascii_uppercase[len(max(table_values, key=len)) - 1]
    lines_number = len(table_values)
    await wrapp_service.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'A1:{column}{lines_number}',
            valueInputOption='USER_ENTERED',
            json={'majorDimension': 'ROWS', 'values': table_values},
        )
    )
