from aiogoogle import Aiogoogle

from .constants import (DISCOVER_DRIVE_V3, DISCOVER_SHEETS_V4,
                        PERMISSIONS_CONFIG, REPORT_DATE,
                        SPREADSHEET_PROPERTIES, SPREADSHEET_URL_TEMPLATE,
                        TABLE_HEADER)
from .validation import validate_table_size


async def create_spreadsheet(wrapp_service: Aiogoogle):

    spreadsheet_properties = SPREADSHEET_PROPERTIES.copy()
    spreadsheet_properties['properties']['title'] = f'Отчет от {REPORT_DATE}'

    service = await wrapp_service.discover(*DISCOVER_SHEETS_V4)
    response = await wrapp_service.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_PROPERTIES)
    )
    response = await wrapp_service.as_service_account(
        service.spreadsheets.create(json=spreadsheet_properties)
    )
    spreadsheet_url = SPREADSHEET_URL_TEMPLATE.format(
        response['spreadsheetId']
    )
    return {
        'spreadsheetId': response['spreadsheetId'],
        'spreadsheetUrl': spreadsheet_url
    }


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
    table_values[0].append(REPORT_DATE)

    for project in projects:
        table_values.append([*project.values()])

    validate_table_size(table_values)

    rows = len(table_values)
    cols = len(table_values[0])

    r1c1_range = f'R1C1:R{rows}C{cols}'

    await wrapp_service.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=r1c1_range,
            valueInputOption='USER_ENTERED',
            json={'majorDimension': 'ROWS', 'values': table_values},
        )
    )
