from datetime import datetime

from aiogoogle import Aiogoogle

from .constants import (COLUMN_COUNT, DATE_FORMAT, DISCOVER_DRIVE_V3,
                        DISCOVER_SHEETS_V4, PERMISSIONS_CONFIG, ROW_COUNT,
                        SPREADSHEET_PROPERTIES, TABLE_HEADER)


async def create_spreadsheet(wrapp_service: Aiogoogle):

    report_date = datetime.now().strftime(DATE_FORMAT)
    spreadsheet_properties = SPREADSHEET_PROPERTIES.copy()
    spreadsheet_properties['properties']['title'] = report_date

    service = await wrapp_service.discover(*DISCOVER_SHEETS_V4)
    response = await wrapp_service.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_PROPERTIES)
    )
    return response['spreadsheetId'], response['spreadsheetUrl']


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

    for project in projects:
        table_values.append([*project.values()])

    rows = len(table_values)
    cols = max(len(row) for row in table_values)

    if rows > ROW_COUNT or cols > COLUMN_COUNT:
        raise ValueError(
            f'Таблица превышает допустимые размеры: {rows}x{cols} '
        )

    await wrapp_service.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{rows}C{cols}',
            valueInputOption='USER_ENTERED',
            json={'majorDimension': 'ROWS', 'values': table_values},
        )
    )
